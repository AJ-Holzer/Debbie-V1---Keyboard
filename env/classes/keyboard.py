import keyboard
from keyboard import KeyboardEvent  # type: ignore[attr-defined]
from typing import Optional

class KB:
    def __init__(self) -> None:
        self.last_event: Optional[KeyboardEvent] = None

    @property
    def key(self) -> KeyboardEvent:
        # Skip repeated events
        while (new_event := keyboard.read_event()) == self.last_event: pass # type: ignore[attr-defined] 

        self.last_event = new_event
        return new_event
