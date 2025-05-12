import socket
import time
import threading

# Classes
from env.classes.connection import Connection

class Heartbeat:
    def __init__(self, conn: Connection, interval: float = 1.0) -> None:
        self._conn: Connection = conn
        self._heartbeat_interval: float = interval

    def send_heartbeat(self) -> None:
        """Send a heartbeat signal to the server."""
        try:
            self._conn.send(b"\x00")  # Heartbeat signal
            print("Heartbeat sent.")
        except socket.error as e:
            print(f"Error sending heartbeat: {e}")

    def _heartbeat_loop(self) -> None:
        """Loop to send heartbeats at regular intervals."""
        while True:
            self.send_heartbeat()
            time.sleep(self._heartbeat_interval)

    def start(self) -> None:
        """Start the heartbeat thread."""
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()
        print("Heartbeat thread started.")
