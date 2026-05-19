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

    print(f"Conectado!")

    bat = await band.read_battery()
    print(f"Batería: {bat}%")

    print("Iniciando FC (esperando 10 segundos)...")
    await band.start_heart_rate(callback=lambda hr: print(f"FC: {hr} bpm"))
    await asyncio.sleep(10)

    reading = await band.get_reading()
    print(f"\nResumen: FC={reading.heart_rate} bpm  Batería={reading.battery}%")

    await band.disconnect()

if __name__ == "__main__":
    mac = sys.argv[1] if len(sys.argv) > 1 else "B8:53:84:35:F7:99"
    asyncio.run(main(mac))
