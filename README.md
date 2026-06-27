# CardKB-as-USB-keyboard

A simple CircuitPython firmware that transforms the M5Stack CardKB into a native USB HID keyboard using a Raspberry Pi Pico. 
---

## 🔌 Hardware Setup

Connect your CardKB keyboard expansion rail to your Raspberry Pi Pico using the pinout matrix below. 

### Wiring Diagram

| CardKB  | Pico Pin (Example) | Description |
| :--- | :--- | :--- |
| **VCC** | VBUS (5V) | Power input |
| **GND** | GND (Pin 38) | Ground reference |
| **SDA** | GP4 (Pin 6) | I2C Data line |
| **SCL** | GP5 (Pin 7) | I2C Clock line |

---

## 🛠️ Requirements & Installation

1. Install **CircuitPython v9.x** (or newer) onto your development board.
2. Copy the repo CircuitPython folder to your CircuitPython drive
---

## 💻 Script Implementation

Save the following code CircuitPython folder as your CircuitPython drive: (includes libraries and code)

---

## 🔍 How It Works Under the Hood

1. **Execution Burst:** The microcontroller detects the state drop, halts its idle state, and instantly requests 2 bytes from register `0x30` via I2C.
2. **HID Translation:** Byte 1 (modifiers) and Byte 2 (HID keycode) are mapped and pushed downstream out the physical USB port to your host PC as standard USB keyboard keystrokes.
3. **Recovery:** The script flashes the LEDs Magenta during processing and resets back to its silent watch state instantly.

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
