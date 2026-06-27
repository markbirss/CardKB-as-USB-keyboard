# CardKB-as-USB-keyboard

An ultra-efficient, interrupt-driven CircuitPython driver that transforms the M5Stack CardKB (Tab5 firmware compatible v2) into a native USB HID keyboard using a Raspberry Pi Pico or similar micro-controller. 

Instead of burning CPU cycles with aggressive I2C polling, this implementation leverages the hardware **INT (Interrupt) pin** to trigger reads strictly on physical key transitions (presses and releases).

---

## ⚡ The Power of the INT Pin

Typical CardKB scripts use constant I2C polling (`i2c.writeto_then_readfrom`) dozens of times per second. This causes significant CPU overhead, system power drain, and potential input lag if your main application loop gets busy.

### Key Benefits of this Implementation:
* **Zero Idle Bus Overhead:** The I2C bus remains dead silent until a physical key event occurs.
* **Eliminates Ghost Key Repeats:** By responding directly to the hardware INT pin transition, it naturally avoids reading the same keyboard buffer byte multiple times.
* **Maximized CPU Availability:** Frees up your microcontroller's processor to run heavy application code (like display rendering or sensor math) without missing keypresses.

---

## 🔌 Hardware Setup

Connect your CardKB keyboard expansion rail to your Raspberry Pi Pico (or compatible board) using the pinout matrix below. 

### Wiring Diagram

| CardKB / Tab5 Pin | Pico Pin (Example) | Description |
| :--- | :--- | :--- |
| **VCC** | 3V3 (Pin 36) or VBUS (5V) | Power input |
| **GND** | GND (Pin 38) | Ground reference |
| **SDA** | GP4 (Pin 6) | I2C Data line |
| **SCL** | GP5 (Pin 7) | I2C Clock line |
| **INT** | **GP3 (Pin 5)** | **Hardware Interrupt Pin** |

> 💡 *Note: The Tab5 INT pin rests **HIGH** when idle and pulls **LOW** the exact millisecond a user presses or releases a key.*

---

## 🛠️ Requirements & Installation

1. Install **CircuitPython v9.x** (or newer) onto your development board.
2. Download the latest Adafruit CircuitPython Bundle.
3. Copy the following library folders/files into your board's `/lib` folder:
   * `adafruit_hid/`
   * `adafruit_bus_device/`

---

## 💻 Script Implementation

Save the following code block as `code.py` on your CircuitPython drive:

```python
import time
import board
import busio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard

# Initialize emulated USB HID Keyboard
kbd = Keyboard(usb_hid.devices)

# Initialize I2C Communication (SCL, SDA)
i2c = busio.I2C(board.GP5, board.GP4)

# Configure the INT pin (Using Pico GP3 as an example)
int_pin = digitalio.DigitalInOut(board.GP3)
int_pin.direction = digitalio.Direction.INPUT
int_pin.pull = digitalio.Pull.UP

# Tab5 / CardKB Constants
TAB5_KB_ADDR = 0x6D
HID_REG = 0x30
LED_REG = 0x60

# Wait for I2C bus lock
while not i2c.try_lock():
    pass

def set_keyboard_led(r, g, b):
    """Updates the onboard dual WS2812E status LEDs."""
    try:
        i2c.writeto(TAB5_KB_ADDR, bytearray([LED_REG, r, g, b]))
    except OSError:
        pass

# Set idle background LED color (Cyan)
print("Tab5 Interrupt-Driven Engine Active!")
set_keyboard_led(0, 40, 40)

# Pre-allocated buffers to prevent memory fragmentation in fast loops
reg_buf = bytearray([HID_REG])
data_buf = bytearray(2)

while True:
    # Crucial Execution Hook: ONLY communicate if the INT pin goes LOW
    if not int_pin.value:
        try:
            # Immediately read the waiting keys from the hardware FIFO queue
            i2c.writeto_then_readfrom(TAB5_KB_ADDR, reg_buf, data_buf)
            
            modifier = data_buf[0]
            key_code = data_buf[1]
            
            # 0xFF represents an empty buffer or a completed 'key release' block
            if modifier != 0xFF and key_code != 0xFF:
                
                # Visual feedback: blink LEDs Magenta during active key processing
                set_keyboard_led(50, 0, 50)
                
                # Process active hardware modifiers
                if modifier > 0:
                    kbd.report[0] = modifier
                
                # Handle standard HID key code dispatch
                if key_code > 0:
                    kbd.press(key_code)
                    kbd.release(key_code)
                    
                # Clean up modifier states
                if modifier > 0:
                    kbd.report[0] = 0
            else:
                # Revert LEDs to standard idle color when key is cleared
                set_keyboard_led(0, 40, 40)
                
        except OSError:
            # Visual warning: Flash amber if an I2C transaction fails
            set_keyboard_led(50, 20, 0)
            
    # Short sleep prevents extreme CPU spinning while maintaining responsiveness
    time.sleep(0.001) 
```

---

## 🔍 How It Works Under the Hood

1. **Idle State:** The microcontroller monitors `int_pin.value`. The I2C lines remain completely inactive. The on-board LEDs glow steady Cyan.
2. **Key Action:** A key is tapped. The CardKB onboard STM32 processor forces the `INT` line low.
3. **Execution Burst:** The microcontroller detects the state drop, halts its idle state, and instantly requests 2 bytes from register `0x30` via I2C.
4. **HID Translation:** Byte 1 (modifiers) and Byte 2 (HID keycode) are mapped and pushed downstream out the physical USB port to your host PC as standard USB keyboard keystrokes.
5. **Recovery:** The script flashes the LEDs Magenta during processing and resets back to its silent watch state instantly.

---

## 🤝 Contributing

Contributions to improve performance, add multi-key rollover maps, or add native hardware async callbacks are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is open-source and licensed under the MIT License.

## ⚠️ Disclaimer
> **Warning:** Use of this project is entirely at your own risk. The project developer accept no liability for hardware damage, malfunctions, or safety hazards resulting from replication.

## ☕ Support My Work
If this open hardware project brings utility to you, consider supporting my design pipeline!

[![Buy Me A Coffee](https://img.shields.io/badge/buy_me_a_coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mark.birss)
