from keyboard import KeyboardEvent, KEY_DOWN, KEY_UP
from typing import Optional

# Classes
from env.classes.connection import Connection
from env.classes.keyboard import KB
from env.classes.heartbeat import Heartbeat

# Config
from env.config import config

def main() -> None:
    conn: Connection = Connection()
    kb: KB = KB()
    heartbeat: Heartbeat = Heartbeat(conn, interval=1.0)
    heartbeat.start()

    while True:
        pressed_key: KeyboardEvent = kb.key
        data: Optional[bytes] = config.controller_map.get(str(pressed_key.name), None)
        if not data: continue

        if pressed_key.event_type == KEY_DOWN:
            print(f"Key pressed: {pressed_key.name}")
            conn.send(data=data)
        elif pressed_key.event_type == KEY_UP:
            print(f"Key released: {pressed_key.name}")
            conn.send(data=b"\xff")  # Send stop command

if __name__ == "__main__": main()
