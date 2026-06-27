# CardKB-as-USB-keyboard

A simple CircuitPython firmware that transforms the M5Stack CardKB into a native USB HID keyboard using a Raspberry Pi Pico. 
---

<img width="1862" height="1604" alt="image" src="https://github.com/user-attachments/assets/72d081e4-97d9-4416-90f7-327fcae0e7f6" />


M5Stack Pinout connection to Raspberry Pi Pico
| CardKB  | Pico Pin (Example) | Description |
| :--- | :--- | :--- |
| **GND** | GND (Pin 38) | Black |
| **VCC** | VBUS (5V) | Red |
| **SDA** | GP4 (Pin 6) | Yellow |
| **SCL** | GP5 (Pin 7) | White |

## 🔌 Hardware Setup

Connect your CardKB keyboard expansion rail to your Raspberry Pi Pico using the pinout matrix below. Copy the CirtcuitPython folder to your CirtcuitPython Drive. Power cycle the Raspberry Pi pico and connect it to your computer USB port. Typing on the keyboard should now work as a normal USB input device

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

## 🤝 Contributing

Contributions to improve performance, add multi-key rollover maps, or add native hardware async callbacks are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is open-source and licensed under the MIT License.

## ⚠️ Disclaimer
> **Warning:** Use of this project is entirely at your own risk. The project developer accept no liability for hardware damage, malfunctions, or safety hazards resulting from replication.

## ☕ Support My Work
If this open hardware project brings utility to you, consider supporting my design pipeline!

[![Buy Me A Coffee](https://img.shields.io/badge/buy_me_a_coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mark.birss)
