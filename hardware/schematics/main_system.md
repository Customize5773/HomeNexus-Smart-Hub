# HomeNexus Smart Hub - Main System Schematic

## Power Distribution System
```mermaid
graph LR
    A[Solar Panel<br>18-24V] --> B[DC-DC Converter]
    B -->|5.1V| C[Power Bank<br>20,000mAh]
    C --> D[Raspberry Pi 5]
    D --> E[Peripherals]
    subgraph Voltage Regulation
        B
    end
    subgraph Backup Power
        C
    end
```

## Sensor Network Architecture
```mermaid
graph TD
    RPI[Raspberry Pi] -->|I²C| MUX[TCA9548A<br>I²C Multiplexer]
    MUX --> INA1[INA219 Ch0<br>Solar Input]
    MUX --> INA2[INA219 Ch1<br>Battery]
    MUX --> INA3[INA219 Ch2<br>Main Load]
    
    RPI -->|SPI| ADC[MCP3008 ADC]
    ADC -->|CH0| LDR[Light Sensor]
    ADC -->|CH1| POT1[Potentiometer]
    
    RPI -->|1-Wire| DS18B20[Temp Sensor]
    RPI -->|GPIO| PIR[PIR Motion]
    RPI -->|GPIO| REED[Reed Switch]
    RPI -->|SPI| RFID[RFID Reader]
```

## Control System Wiring
```mermaid
graph LR
    RPI[RPi GPIO] -->|PWM| FAN[Cooling Fan]
    RPI -->|PWM| SERVO[Door Servo]
    RPI -->|Digital| HEATER[Heating Pad]
    RPI -->|PWM| LED1[LED 1]
    RPI -->|PWM| LED2[LED 2]
    RPI -->|PWM| LED3[LED 3]
    
    subgraph Transistor Drivers
        FAN
        HEATER
    end
```

## Detailed Component Schematics

### INA219 Power Monitor Circuit
```
     Solar/Battery + ───────────────╮
                                    │
     ╭───────────────┬───────────────┤
     │               │               │
     │            ┌──┴──┐        ┌───┴──┐
     │            │     │        │      │
     ├────────────┤ IN+ ├────────┤ Vin+ │
     │            │     │        │      │
     │            └──┬──┘        └──┬───┘
     │               │              │   INA219
     │            ┌──┴──┐        ┌──┴───┐
     │            │     │        │      │
     ├────────────┤ IN- ├────────┤ Vin- │
     │            │     │        │      │
     │            └─────┘        └──┬───┘
     │               │              │
     ╰───────────────┴──────────────┤
                                    │
     Load + ────────────────────────╯
```

### LED Control Circuit
```
GPIO (3.3V) ─── 220Ω ───┬── LED+ 
                        │
                        ├── 1N5819 Diode (reverse protection)
                        │
GND ────────────────────┴── LED-
```

### Fan Control Circuit
```
GPIO (PWM) ─── 100Ω ───┬── Base (SS8050)
                       │
5V ────────────────────┼── Collector
                       │
GND ───────────────────┴── Emitter ─── Fan- 
                       │
                       └── Fan+ ───── 5V
```

### Temperature Sensor Wiring
```
3.3V ───────────────╮
                    │
                    ├── 4.7kΩ ─── GPIO4
                    │
DS18B20 Data ───────╯
                    │
DS18B20 GND ─────── GND
```

## Verification Points
| Test Point | Expected Value | Measurement Tip |
|------------|----------------|-----------------|
| DC-DC Output | 5.1V ±0.1V | Measure at power bank input |
| GPIO High | 3.3V | No load condition |
| I²C SDA/SCL | Pulsed 3.3V | Use oscilloscope |
| Servo Signal | 50Hz PWM | Duty cycle 2.5-12.5% |

> **Safety Notice**: Always disconnect solar input before making wiring changes. Use 20AWG wire for all power connections.
