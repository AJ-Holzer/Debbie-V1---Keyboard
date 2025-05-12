import socket
import time
import threading
from typing import Optional

# Config
from env.config import config

class Connection:
    def __init__(self) -> None:
        self.sock: Optional[socket.socket] = None
        self._lock = threading.Lock()
        self._connect()

    def _connect(self) -> None:
        """(Re)initialize the socket connection."""
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                print(f"Connecting to {config.server_ip}:{config.server_port}...")
                s.connect((config.server_ip, config.server_port))
                s.settimeout(None)  # Disable timeout after connection
                self.sock = s
                print("Connected.")
                break
            except (socket.error, ConnectionRefusedError) as e:
                print(f"Connection failed ({e}). Retrying in 2 seconds...")
                time.sleep(2)

    def send(self, data: bytes) -> None:
        while True:
            try:
                with self._lock:
                    if self.sock is None:
                        self._connect()
                        continue
                    self.sock.sendall(data)
                break
            except (BrokenPipeError, ConnectionResetError, socket.error) as e:
                print(f"Send failed ({e}). Reconnecting...")
                self._connect()

    def receive(self, bufsize: int = 1024) -> bytes:
        while True:
            try:
                with self._lock:
                    if self.sock is None:
                        self._connect()
                        continue
                    return self.sock.recv(bufsize)
            except (BrokenPipeError, ConnectionResetError, socket.error) as e:
                print(f"Receive failed ({e}). Reconnecting...")
                self._connect()
