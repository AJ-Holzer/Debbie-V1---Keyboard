import evdev
from evdev import InputDevice, categorize, ecodes
from typing import Optional

def get_keyboard_device() -> Optional[InputDevice]:
    """Finds and returns the first keyboard device."""
    for device_path in evdev.list_devices():
        device = InputDevice(device_path)
        if ecodes.EV_KEY in device.capabilities():
            return device
    return None

def read_keypresses(device: InputDevice) -> str:
    """Reads key presses from the given device and returns them as a string."""
    pressed_keys = []
    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    key_name = evdev.ecodes.KEY[event.code][4:]
                    pressed_keys.append(key_name)
                    return "".join(pressed_keys)
    except KeyboardInterrupt:
        print("\nStopping key listener.")
    return ""  # Return empty string if interrupted

def main() -> None:
    """Main function to initialize and run key press detection."""
    device = get_keyboard_device()
    if not device:
        print("No keyboard device found.")
        return
    print(f"Listening for key presses on: {device.path}")
    while True:
        key_string = read_keypresses(device)
        if key_string:
            print(f"Keys Pressed: {key_string}")

if __name__ == "__main__":
    main()
