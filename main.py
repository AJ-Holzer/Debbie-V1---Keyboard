import evdev
from evdev import InputDevice, categorize, ecodes
from typing import Optional
from flask import Flask, jsonify

app = Flask(__name__)
pressed_keys = []

def get_keyboard_device() -> Optional[InputDevice]:
    """Finds and returns the first keyboard device."""
    for device_path in evdev.list_devices():
        device = InputDevice(device_path)
        if ecodes.EV_KEY in device.capabilities():
            return device
    return None

def read_keypresses(device: InputDevice) -> None:
    """Reads key presses from the given device and stores them."""
    global pressed_keys
    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    key_name = evdev.ecodes.KEY[event.code][4:]
                    pressed_keys.append(key_name)
    except KeyboardInterrupt:
        print("\nStopping key listener.")

@app.route('/keys', methods=['GET'])
def get_keys():
    """Returns the pressed keys as JSON."""
    return jsonify({"pressed_keys": pressed_keys})

def main() -> None:
    """Main function to initialize and run key press detection."""
    device = get_keyboard_device()
    if not device:
        print("No keyboard device found.")
        return
    print(f"Listening for key presses on: {device.path}")
    read_keypresses(device)

if __name__ == "__main__":
    from threading import Thread
    thread = Thread(target=main)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
