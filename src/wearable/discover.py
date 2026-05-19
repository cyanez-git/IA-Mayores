"""
Script de descubrimiento BLE — correr cuando llega el Xiaomi Smart Band 9 Active.
Escanea dispositivos cercanos y muestra MAC, nombre y servicios disponibles.

Uso:
    python src/wearable/discover.py              # escanea 10 segundos
    python src/wearable/discover.py --dump MAC   # muestra todos los servicios del dispositivo
"""
import asyncio
import argparse
import sys
from bleak import BleakScanner, BleakClient


async def scan(duration: int = 10):
    print(f"[BLE] Escaneando dispositivos por {duration} segundos...\n")
    devices = await BleakScanner.discover(timeout=duration)

    xiaomi = []
    others = []

    for d in devices:
        name = d.name or "Sin nombre"
        if any(k in name.lower() for k in ["mi band", "xiaomi", "smart band", "mi smart", "band 9"]):
            xiaomi.append(d)
        else:
            others.append(d)

    if xiaomi:
        print("=== Dispositivos Xiaomi encontrados ===")
        for d in xiaomi:
            print(f"  📱 {d.name}")
            print(f"     MAC: {d.address}")
            print(f"     RSSI: {getattr(d, 'rssi', 'N/A')} dBm")
            print()
    else:
        print("No se encontraron dispositivos Xiaomi.\n")
        print("Asegurate de que el Smart Band esté desbloqueado y cerca.\n")

    if others:
        print(f"Otros dispositivos encontrados: {len(others)}")
        for d in others:
            print(f"  - {d.name or 'Sin nombre'} ({d.address})")

    return xiaomi


async def dump_services(mac: str):
    print(f"[BLE] Conectando a {mac} para listar servicios...\n")
    async with BleakClient(mac) as client:
        print(f"Conectado: {client.is_connected}\n")
        for service in client.services:
            print(f"Servicio: {service.uuid}")
            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"  Característica: {char.uuid}  [{props}]")
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", metavar="MAC", help="Volcar servicios de un dispositivo por MAC")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()

    if args.dump:
        asyncio.run(dump_services(args.dump))
    else:
        found = asyncio.run(scan(args.timeout))
        if found:
            print("\nPróximo paso:")
            print(f"  python src/wearable/discover.py --dump {found[0].address}")
