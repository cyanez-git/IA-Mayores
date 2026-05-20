"""
Emparejamiento inicial del Xiaomi Smart Band 9 Active.
Correr DESPUÉS de hacer reset de fábrica en el band.

Uso: python3 src/wearable/pair_band.py B8:53:84:35:F7:99
"""
import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

from bleak import BleakClient

MAC = "B8:53:84:35:F7:99"

# Servicio auth clásico Xiaomi (fdab)
UUID_AUTH_NOTIFY  = "00000002-0000-1000-8000-00805f9b34fb"
UUID_AUTH_READ    = "00000001-0000-1000-8000-00805f9b34fb"
UUID_AUTH_WRITE   = "00000003-0000-1000-8000-00805f9b34fb"

# Servicio Xiaomi privado moderno (fe95)
UUID_FE95_READ    = "00000050-0000-1000-8000-00805f9b34fb"
UUID_FE95_NOTIFY  = "0000005e-0000-1000-8000-00805f9b34fb"
UUID_FE95_WRITE   = "0000005f-0000-1000-8000-00805f9b34fb"


async def pair(mac: str):
    print(f"\nConectando a {mac} (band debe estar en modo emparejamiento)...\n")

    async with BleakClient(mac, timeout=20.0) as client:
        print(f"Conectado: {client.is_connected}\n")

        # 1. Leer característica 00000001 del servicio fdab
        print("=== Leyendo UUID_AUTH_READ (00000001) ===")
        try:
            data = await asyncio.wait_for(
                client.read_gatt_char(UUID_AUTH_READ), timeout=5.0
            )
            print(f"  Valor hex: {data.hex()}")
            print(f"  Valor raw: {list(data)}")
            if len(data) in (16, 32):
                key_hex = data.hex()
                print(f"\n  *** POSIBLE AUTH KEY: {key_hex} ***\n")
                _save_key(key_hex)
        except asyncio.TimeoutError:
            print("  Timeout")
        except Exception as e:
            print(f"  Error: {e}")

        # 2. Leer característica 00000050 del servicio fe95
        print("=== Leyendo UUID_FE95_READ (00000050) ===")
        try:
            data = await asyncio.wait_for(
                client.read_gatt_char(UUID_FE95_READ), timeout=5.0
            )
            print(f"  Valor hex: {data.hex()}")
            print(f"  Valor raw: {list(data)}")
        except asyncio.TimeoutError:
            print("  Timeout")
        except Exception as e:
            print(f"  Error: {e}")

        # 3. Suscribir a notificaciones del servicio fdab y enviar señal de inicio
        print("\n=== Iniciando handshake fdab ===")
        received = []

        def on_notify(sender, data: bytearray):
            print(f"  [NOTIFY fdab] {data.hex()}  raw={list(data)}")
            received.append(bytes(data))

        try:
            await client.start_notify(UUID_AUTH_NOTIFY, on_notify)
            # Señal de inicio de emparejamiento
            await client.write_gatt_char(UUID_AUTH_WRITE, bytes([0x01, 0x00]), response=False)
            print("  Señal de inicio enviada — esperando respuesta del band (5s)...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"  Error en handshake fdab: {e}")

        # 4. Suscribir a notificaciones del servicio fe95
        print("\n=== Iniciando handshake fe95 ===")

        def on_fe95(sender, data: bytearray):
            print(f"  [NOTIFY fe95] {data.hex()}  raw={list(data)}")

        try:
            await client.start_notify(UUID_FE95_NOTIFY, on_fe95)
            # Señal de inicio protocolo moderno
            await client.write_gatt_char(UUID_FE95_WRITE, bytes([0x00]), response=False)
            print("  Señal fe95 enviada — esperando respuesta (5s)...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"  Error en handshake fe95: {e}")

        print("\n=== Resumen ===")
        print(f"Paquetes recibidos en fdab: {len(received)}")
        for i, pkt in enumerate(received):
            print(f"  [{i}] {pkt.hex()}")

        print("\nDesconectando...")

    print("Listo. Revisá la salida — si apareció '*** POSIBLE AUTH KEY ***' guardala en .env")


def _save_key(key_hex: str):
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    env_path = os.path.abspath(env_path)

    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("XIAOMI_AUTH_KEY="):
                lines[i] = f"XIAOMI_AUTH_KEY={key_hex}\n"
                found = True
                break

    if not found:
        lines.append(f"XIAOMI_AUTH_KEY={key_hex}\n")

    with open(env_path, 'w') as f:
        f.writelines(lines)

    print(f"  Auth key guardada en {env_path}")


if __name__ == "__main__":
    mac = sys.argv[1] if len(sys.argv) > 1 else MAC
    asyncio.run(pair(mac))
