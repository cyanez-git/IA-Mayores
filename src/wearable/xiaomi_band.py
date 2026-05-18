"""
Integración Xiaomi Smart Band 9 Active vía BLE (bleak).

Protocolo basado en reverse engineering de la comunidad para Mi Band 7/8/9.
Requiere AUTH_KEY de 16 bytes — ver instrucciones abajo.

Cómo obtener el AUTH_KEY:
  1. Instalar Mi Fitness en el teléfono y vincular el Smart Band
  2. En Android con ADB: adb logcat | grep -i "auth\|key\|band"
     o usar la app "Mi Band Tools" que muestra la clave directamente
  3. Guardar la clave en .env: XIAOMI_AUTH_KEY=tu_clave_hex_aqui
"""
import asyncio
import hashlib
import hmac
import logging
import os
import struct
import time
from dataclasses import dataclass

from bleak import BleakClient, BleakScanner

log = logging.getLogger(__name__)

# UUIDs del Xiaomi Smart Band 7/8/9
UUID_SERVICE_MAIN    = "0000fee0-0000-1000-8000-00805f9b34fb"
UUID_AUTH_CHAR       = "00000009-0000-3512-2118-0009af100700"
UUID_HR_MEASURE      = "00002a37-0000-1000-8000-00805f9b34fb"
UUID_HR_CONTROL      = "00002a39-0000-1000-8000-00805f9b34fb"
UUID_STEPS           = "00000007-0000-3512-2118-0009af100700"
UUID_BATTERY         = "00000006-0000-3512-2118-0009af100700"
UUID_SENSOR_DATA     = "00000001-0000-3512-2118-0009af100700"

AUTH_CMD_REQUEST     = bytes([0x02, 0x00])
AUTH_CMD_RESPONSE    = bytes([0x03, 0x00])
HR_START_CONTINUOUS  = bytes([0x15, 0x01, 0x01])
HR_STOP_CONTINUOUS   = bytes([0x15, 0x01, 0x00])


@dataclass
class BandReading:
    heart_rate: int
    steps: int
    battery: int       # porcentaje
    accel_x: float
    accel_y: float
    accel_z: float
    impact_detected: bool
    timestamp: float


class XiaomiBand:
    def __init__(self, mac: str, auth_key: str = ""):
        self.mac = mac
        self.auth_key = bytes.fromhex(auth_key) if auth_key else None
        self._client: BleakClient | None = None
        self._hr = 0
        self._steps = 0
        self._battery = 0
        self._accel = (0.0, 0.0, 1.0)
        self._authenticated = False

    async def connect(self) -> bool:
        try:
            self._client = BleakClient(self.mac, timeout=15.0)
            await self._client.connect()
            log.info(f"[Band] Conectado a {self.mac}")

            if self.auth_key:
                await self._authenticate()
            else:
                log.warning("[Band] Sin auth_key — funciones limitadas")
                self._authenticated = True

            return self._client.is_connected
        except Exception as e:
            log.error(f"[Band] Error al conectar: {e}")
            return False

    async def _authenticate(self):
        """Protocolo de autenticación Mi Band 7/8/9."""
        auth_event = asyncio.Event()
        auth_ok = [False]

        def on_auth(sender, data: bytearray):
            if data[:3] == bytes([0x10, 0x02, 0x01]):
                # Recibimos número random — ciframos con HMAC-SHA256
                rnd = bytes(data[3:])
                key = hmac.new(self.auth_key, rnd, hashlib.sha256).digest()
                asyncio.ensure_future(
                    self._client.write_gatt_char(
                        UUID_AUTH_CHAR, AUTH_CMD_RESPONSE + key
                    )
                )
            elif data[:3] == bytes([0x10, 0x03, 0x01]):
                log.info("[Band] Autenticado correctamente")
                auth_ok[0] = True
                auth_event.set()
            elif data[:3] == bytes([0x10, 0x03, 0x04]):
                log.error("[Band] Auth falló — AUTH_KEY incorrecta")
                auth_event.set()

        await self._client.start_notify(UUID_AUTH_CHAR, on_auth)
        await self._client.write_gatt_char(UUID_AUTH_CHAR, AUTH_CMD_REQUEST)

        try:
            await asyncio.wait_for(auth_event.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            log.error("[Band] Timeout en autenticación")

        self._authenticated = auth_ok[0]

    async def read_battery(self) -> int:
        try:
            data = await self._client.read_gatt_char(UUID_BATTERY)
            self._battery = data[1]
            return self._battery
        except Exception:
            return 0

    async def read_steps(self) -> int:
        try:
            data = await self._client.read_gatt_char(UUID_STEPS)
            self._steps = struct.unpack_from("<I", data, 1)[0]
            return self._steps
        except Exception:
            return 0

    async def start_heart_rate(self, callback=None):
        """Inicia monitoreo continuo de FC. callback(hr: int) se llama con cada lectura."""
        def on_hr(sender, data: bytearray):
            if len(data) >= 2:
                hr = data[1]
                if hr > 0:
                    self._hr = hr
                    if callback:
                        callback(hr)

        await self._client.start_notify(UUID_HR_MEASURE, on_hr)
        await self._client.write_gatt_char(UUID_HR_CONTROL, HR_START_CONTINUOUS)
        log.info("[Band] Monitoreo FC iniciado")

    async def stop_heart_rate(self):
        await self._client.write_gatt_char(UUID_HR_CONTROL, HR_STOP_CONTINUOUS)
        await self._client.stop_notify(UUID_HR_MEASURE)

    async def get_reading(self) -> BandReading:
        ax, ay, az = self._accel
        impact = (ax**2 + ay**2 + az**2) ** 0.5 > 2.5
        return BandReading(
            heart_rate=self._hr,
            steps=self._steps,
            battery=self._battery,
            accel_x=round(ax, 3),
            accel_y=round(ay, 3),
            accel_z=round(az, 3),
            impact_detected=impact,
            timestamp=time.time(),
        )

    async def disconnect(self):
        if self._client and self._client.is_connected:
            await self.stop_heart_rate()
            await self._client.disconnect()
            log.info("[Band] Desconectado")


async def find_band(timeout: int = 10) -> str | None:
    """Escanea y retorna la MAC del primer Smart Band Xiaomi encontrado."""
    print(f"[Band] Buscando Smart Band ({timeout}s)...")
    devices = await BleakScanner.discover(timeout=timeout)
    for d in devices:
        name = (d.name or "").lower()
        if any(k in name for k in ["mi band", "smart band", "band 9"]):
            print(f"[Band] Encontrado: {d.name} → {d.address}")
            return d.address
    print("[Band] No se encontró ningún dispositivo Xiaomi.")
    return None
