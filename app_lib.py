import asyncio
from bleak import BleakScanner, BleakClient
import sys

async def scan():
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == "DSD TECH":
                print(device)
    except TimeoutError as e:
        print(e)
        sys.exit()

asyncio.run(scan())

async def send(client,character, message):
    try:
        await client.write_gatt_char(character,message.encode('utf-8'))
    except Exception as e:
        print(e)

async def connect(address,character):
    async with BleakClient(address) as client:
        print("Connected to Device")
        if client.is_connected:
            # services = client.services
            # for service in services:
            #     print(f"Service: {service.uuid}")
            #     for char in service.characteristics:
            #         props = ", ".join(char.properties)
            #         print(f"   Characteristic: {char.uuid} (Properties: {props})")
            message = input("Write Message: ")
            await send(client, character, message)

if __name__ == "__main__":
    address = "F8:30:02:39:BD:05"
    character = "0000ffe1-0000-1000-8000-00805f9b34fb"
    asyncio.run(connect(address,character))
