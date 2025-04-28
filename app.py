import tkinter as tk
#from app_lib import scan, send
import asyncio
import sys
import threading
from bleak import BleakClient, BleakScanner

client = None
characteristic = None
connected = False

class Redirector:
    def __init__(self, text_widget):
        self.text = text_widget

    def write(self, string):
        self.text.insert(tk.END, string)
        self.text.see(tk.END)

    def flush(self):
        pass

def notification(sender, data):
    log(f"From {sender}: {data.decode(errors='ignore')}")

def connect(add, log):
    def run():
        global client, characteristic, connected
        try:
            log("Attempting to Connect")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = BleakClient(add)
            loop.run_until_complete(client.connect())
            connected = client.is_connected
            if connected:
                log("Connected to Device")
                loop.run_until_complete(client.start_notify(characteristic, notification))
                while connected:
                    loop.run_until_complete(asyncio.sleep(.1))
            else:
                log("Could not Connect")
        except Exception as e:
            log(f"Error: {e}")
    threading.Thread(target=run, daemon=True).start()


def start_scan(set_device, log):
    def run():
        try:
            log("Starting Scan")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            devices = loop.run_until_complete(BleakScanner.discover(timeout=5.0))
            results = []
            for device in devices:
                if device.name == "DSD TECH":
                    results.append((device.name, device.address))
            set_device(results)

        except Exception as e:
            log(f"Error Scanning: {e}")
        log("Completed Scan")
    threading.Thread(target=run).start()

def send(log, message):
    def run():
        global client, characteristic
        try:
            log(f"Sending Message: {message}")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if message[0] == 'g':
                loop.run_until_complete(client.write_gatt_char(characteristic, message.encode('utf-8')))
                #log("Message Sent")
            if message[0] == 'i':
                loop.run_until_complete(client.write_gatt_char(characteristic, message.encode('utf-8')))

        except Exception as e:
            log(f"Error Sending Message: {e}")
    threading.Thread(target=run).start()

root = tk.Tk()
root.title("MSPM0 Desktop Application")
root.configure(bg="red")

box = tk.Text(root, height=15, width = 60)
box.pack(padx = 10, pady = 10)

def clear_text():
    box.delete(1.0, tk.END)

clear_button = tk.Button(text="Clear Text", command=clear_text)
clear_button.pack(pady=5)

listlabel = tk.Label(root, text="Device List", bg="red").pack()

device_box = tk.Listbox(root, height=6, width = 60)
device_box.pack(pady=5)

selected = tk.StringVar()

def on_select(event):
    selection = device_box.curselection()
    if selection:
        index = selection[0]
        _, addr = device_box.devices[index]
        selected.set(addr)
    
device_box.bind("<<ListboxSelect>>", on_select)

# char_entry = tk.Entry(root, width=60)
# char_entry.pack(pady=5)
characteristic = "0000ffe1-0000-1000-8000-00805f9b34fb"

def set_list(devices):
    device_box.delete(0, tk.END)
    for name, addr in devices:
        device_box.insert(tk.END, f"{name} - {addr}")
    device_box.devices = devices

def log(msg):
    box.insert(tk.END, msg + "\n")
    box.see(tk.END)

sys.stdout = Redirector(box)

scan_button = tk.Button(root, text="Start Scan", bg="white", command=lambda: start_scan(set_list,log))
scan_button.pack(padx = 20, pady=10)

connect_button = tk.Button(root, text="Connect", bg="white", command=lambda: connect(selected.get(), log))
connect_button.pack(padx = 20, pady = 10)

gpio_label = tk.Label(root, text = "GPIO Buttons", bg="red")
gpio_label.pack()

gpio_row = tk.Frame(root, bg="red")
gpio_row.pack(pady=10)

red = tk.Button(gpio_row, text="Red", command=lambda: send(log, "gR"))
green = tk.Button(gpio_row, text="Green", command=lambda: send(log, "gG"))
blue = tk.Button(gpio_row, text="Blue", command=lambda: send(log, "gB"))
mono = tk.Button(gpio_row, text="Mono", command=lambda: send(log, "gM"))

red.pack(side="left", padx=10)
green.pack(side="left", padx=10)
blue.pack(side="left", padx=10)
mono.pack(side="left", padx=10)

dht22_label = tk.Label(root, text="DHT22" ,bg="red")
dht22_label.pack(pady=10)

dht22_row = tk.Frame(root, bg="red")
dht22_row.pack(pady=10)

temp = tk.Button(dht22_row, text="Temp")
hum = tk.Button(dht22_row, text="Humidity")

temp.pack(side="left",padx=10)
hum.pack(side="left",padx=10)

root.mainloop()