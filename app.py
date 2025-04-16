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

def connect(add, log):
    def run():
        global client, characteristic, connected
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = BleakClient(add)
            loop.run_until_complete(client.connect())
            connected = client.is_connected

            if connected:
                log("Connected to Device")
            else:
                log("Could not Connect")
        except Exception as e:
            log(f"Error: {e}")
    threading.Thread(target=run).start()


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

root = tk.Tk()
root.title("MSPM0 Desktop Application")
root.configure(bg="red")

box = tk.Text(root, height=15, width = 60)
box.pack(padx = 10, pady = 20)

listlabel = tk.Label(root, text="Device List").pack()

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

scan_button = tk.Button(root, text="Start Scan", command=lambda: start_scan(set_list,log))
scan_button.pack(padx = 20, pady=20)

connect_button = tk.Button(root, text="Connect", command=lambda: connect(selected.get(), log))
connect_button.pack(padx = 20, pady = 20)

root.mainloop()