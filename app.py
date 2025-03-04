import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name != None:
            print(device)

asyncio.run(scan())
