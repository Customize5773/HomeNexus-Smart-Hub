# HomeNexus Smart Hub - Hardware Assembly Guide

## 1. Bill of Materials
Verify you have all components before starting:

| Category        | Components |
|-----------------|------------|
| **Core**        | Raspberry Pi 5, 16GB microSD, USB-C PSU |
| **Power**       | Solar panel, 20,000mAh power bank, DC-DC converter |
| **Sensors**     | DS18B20, LDR, PIR, Reed switch, RFID reader |
| **Controls**    | 6x LEDs, Cooling fan, Heating pad, Servo |
| **Electronics** | MCP3008 ADC, TCA9548A I²C Mux, Resistors, Transistors |

## 2. Base Platform Construction
### Playmobil House Mounting
1. **Cut MDF base** to 30x25cm (adjust for your house size)
2. **Attach hinges** to back wall for easy access:
   ```python
   # Hinge placement diagram
   [House] ====||==== [Base]
            Hinge x2
   ```
3. **Create component zones**:
   - Left side: Power system
   - Center: Raspberry Pi
   - Right: Sensor array

## 3. Power System Assembly
### Solar Integration
```mermaid
graph LR
    A[Solar Panel] --> B[DC-DC Converter]
    B --> C[Power Bank]
    C --> D[Raspberry Pi]
    D --> E[Peripherals]
```

1. **Wire solar panel** to converter's input (18-24V)
2. **Set converter output** to 5.1V (adjust trim pot)
3. **Connect power bank** to converter output
4. **Verify charging** with multimeter (5.0-5.2V)

## 4. Sensor Network Installation
### Temperature Sensor (DS18B20)
1. Enable 1-Wire interface:
   ```bash
   sudo raspi-config
   # Interface Options → 1-Wire → Enable
   ```
2. Wire configuration:
   ```
   DS18B20 Pinout:
   Red   → 3.3V
   Black → GND
   Yellow → GPIO4 (with 4.7kΩ pull-up)
   ```

### Light Sensor (LDR)
```
   LDR Circuit:
   3.3V —— LDR ——-||——- 10kΩ —— GND
               ADC Input (MCP3008 CH0)
```

## 5. Control Module Wiring
### LED Matrix
```python
# GPIO Mapping (BCM):
LEDS = [5, 6, 13, 19, 26, 21]  # Update in config.py
```
1. Use 220Ω current-limiting resistors
2. Common cathode configuration

### Servo Door Lock
```
SG90 Wiring:
Brown  → GND
Red    → 5V
Orange → GPIO12 (PWM)
```

## 6. Final Assembly Steps
1. **Secure all components** with hot glue
2. **Route cables** through cable channels
3. **Test each subsystem**:
   ```bash
   # Quick diagnostic
   python3 -c "from drivers.sensors import TemperatureSensor; print(TemperatureSensor().read())"
   ```

## 7. Safety Checks
- [ ] Verify no exposed conductors
- [ ] Confirm proper heat dissipation
- [ ] Test emergency shutdown (hold button for 3s)

## Troubleshooting
| Symptom | Solution |
|---------|----------|
| No power | Check DC-DC converter output |
| Sensor failures | Verify I²C addresses with `i2cdetect -y 1` |
| RF interference | Add ferrite beads to power lines |

> **Pro Tip**: Use color-coded Dupont cables (Red=5V, Black=GND, Yellow=Signal)
