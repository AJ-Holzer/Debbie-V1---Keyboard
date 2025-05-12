from typing import Literal

class Config:
    def __init__(self) -> None:
        # Connection settings
        # self.server_ip: str = f"https://debbie.ajservers.site:8443/controller/"
        self.server_ip: str = "192.168.8.4"
        self.server_port: int = 58_000
        self.bufsize: int = 1024

        # Keyboard settings
        self.controller_map: dict[str, bytes] = {
            "w":           b"\x01",  # Walk forwards
            "s":           b"\x02",  # Walk backwards
            "left":  b"\x03",  # Turn left
            "right": b"\x04",  # Turn right
            "a":           b"\x05",  # Sidestep left
            "d":           b"\x06",  # Sidestep right
            "shift":    b"\x07",  # Lower the legs
            "space":       b"\x08",  # Lift the legs
            "esc":         b"\x09",  # Normal position
        }

config = Config()
