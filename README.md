# HomeNexus-Smart-Hub

<img width="768" height="512" alt="HomeNexus" src="https://github.com/user-attachments/assets/55eb2d52-32fb-4e95-88b6-eea6ac95101d" />

HomeNexus Smart Hub is a comprehensive, Raspberry Pi-based home automation system designed to intelligently manage and monitor your home environment. It integrates various sensors and controls to automate lighting, temperature, security, and power management, all powered by a sustainable solar energy system.

## Features

- **Intelligent Automation:** The system uses a rule-based engine to automate various tasks based on sensor data, such as temperature, light levels, and motion.
- **Power Management:** A sophisticated power management system optimizes energy usage, switching between power profiles based on solar power availability and battery levels.
- **Security:** The hub includes an RFID-based access control system and motion detection to enhance home security.
- **Modular Design:** The project is built with a modular architecture, making it easy to extend and customize with additional sensors and controls.
- **Comprehensive Documentation:** The project includes detailed wiring diagrams, a bill of materials, and a setup guide to help you get started.

## Getting Started

### Prerequisites

- Raspberry Pi 5 with a 16GB microSD card
- A comprehensive set of electronic components (see the [Bill of Materials](hardware/bill_of_materials.md) for a complete list)
- Basic knowledge of electronics and Python programming

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Customize5773/HomeNexus-Smart-Hub.git
   cd HomeNexus-Smart-Hub
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r firmware/requirements.txt
   ```

3. **Set up the hardware:**
   - Follow the [Hardware Assembly Guide](docs/setup_guide.md) to assemble the components.
   - Refer to the [wiring diagrams](docs/wiring_diagrams) for detailed instructions on how to connect the sensors and controls.

4. **Configure the system:**
   - Edit the `firmware/config.py` file to match your specific hardware setup and preferences.

5. **Run the main application:**
   ```bash
   python firmware/main.py
   ```

## Hardware

The HomeNexus Smart Hub is built using a variety of electronic components, including:

- **Core:** Raspberry Pi 5, 16GB microSD, USB-C PSU
- **Power:** Solar panel, 20,000mAh power bank, DC-DC converter
- **Sensors:** DS18B20, LDR, PIR, Reed switch, RFID reader
- **Controls:** 6x LEDs, Cooling fan, Heating pad, Servo
- **Electronics:** MCP3008 ADC, TCA9548A I²C Mux, Resistors, Transistors

For a complete list of components, see the [Bill of Materials](hardware/bill_of_materials.md).

## Software

The software for the HomeNexus Smart Hub is written in Python and is divided into three main components:

- **Firmware:** The main application that runs on the Raspberry Pi, responsible for reading sensor data, executing automation rules, and managing the system.
- **Core:** The core logic of the system, including the automation engine and power manager.
- **Drivers:** A collection of drivers for interacting with the various hardware components, such as sensors, displays, and RFID readers.
