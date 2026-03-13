import os
from .base import BaseDisplay

def get_display() -> BaseDisplay:
    emulate = os.getenv("EINK_EMULATE", "1") != "0"

    if emulate:
        from .emulator import EmulatorDisplay
        return EmulatorDisplay()
    else:
        from .waveshare import WaveshareDisplay
        return WaveshareDisplay()