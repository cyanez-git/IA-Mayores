"""
Test rápido del Smart Band 9 Active — lee batería y FC.
Uso: python3 src/wearable/test_band.py B8:53:84:35:F7:99
"""
import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

from src.wearable.xiaomi_band import XiaomiBand

async def main(mac: str):
    auth_key = os.getenv("XIAOMI_AUTH_KEY", "")
    band = XiaomiBand(mac, auth_key)

    print(f"\nConectando a {mac}...")
    ok = await band.connect()
    if not ok:
        print("No se pudo conectar.")
        return

    print("Conectado!\n")

    # Batería — funciona sin auth key (BLE estándar)
    print("Leyendo batería...")
    bat = await band.read_battery()
    if bat > 0:
        print(f"  Batería: {bat}%")
    else:
        print("  Batería: no disponible")

    # FC — requiere auth key
    if not auth_key:
        print("\nFC: omitido (no hay XIAOMI_AUTH_KEY)")
        print("  → Obtené la clave con Gadgetbridge y configurá XIAOMI_AUTH_KEY en .env")
    else:
        print("\nIniciando FC (esperando 10 segundos)...")
        hr_started = await band.start_heart_rate(callback=lambda hr: print(f"  FC: {hr} bpm"))
        if hr_started:
            await asyncio.sleep(10)
        else:
            print("  FC: no disponible — verificá la auth key")

    reading = await band.get_reading()
    print(f"\n{'='*40}")
    print(f"  FC:      {reading.heart_rate} bpm" if reading.heart_rate else "  FC:      —")
    print(f"  Batería: {reading.battery}%" if reading.battery else "  Batería: —")
    print(f"{'='*40}\n")

    await band.disconnect()

if __name__ == "__main__":
    mac = sys.argv[1] if len(sys.argv) > 1 else "B8:53:84:35:F7:99"
    asyncio.run(main(mac))
