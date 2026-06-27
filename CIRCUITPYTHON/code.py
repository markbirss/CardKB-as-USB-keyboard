import time
import board
import busio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize USB HID Keyboard emulation over the USB port
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Explicitly initialize I2C on Pico GP4 (SDA) and GP5 (SCL)
i2c = busio.I2C(board.GP5, board.GP4)
CARDKB_ADDR = 0x5F

# Wait for I2C lock
while not i2c.try_lock():
    pass

# Target array buffer for reading 1 byte
buf = bytearray(1)

while True:
    try:
        # Read character byte from CardKB
        i2c.readfrom_into(CARDKB_ADDR, buf)
        char_code = buf[0]

        if char_code != 0:
            # Map specific system key strokes
            if char_code == 0x08:      # Backspace
                kbd.send(Keycode.BACKSPACE)
            elif char_code == 0x0D:    # Return/Enter
                kbd.send(Keycode.ENTER)
            elif char_code == 0x09:    # Tab
                kbd.send(Keycode.TAB)
            elif char_code == 0x1B:    # Escape
                kbd.send(Keycode.ESCAPE)

            # Map CardKB Arrow Keys
            elif char_code == 0xB5:    # Up Arrow
                kbd.send(Keycode.UP_ARROW)
            elif char_code == 0xB6:    # Down Arrow
                kbd.send(Keycode.DOWN_ARROW)
            elif char_code == 0xB4:    # Left Arrow
                kbd.send(Keycode.LEFT_ARROW)
            elif char_code == 0xB7:    # Right Arrow
                kbd.send(Keycode.RIGHT_ARROW)

            else:
                # Type standard letters, numbers, and symbols
                layout.write(chr(char_code))

        time.sleep(0.01) # Low polling latency

    except OSError:
        # Gracefully handle temporary wire disconnects
        time.sleep(0.1)
