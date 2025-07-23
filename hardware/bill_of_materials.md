# HomeNexus Smart Hub - Bill of Materials

## Core Components
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| Raspberry Pi 5 | 1 | 8GB RAM | Main controller |
| Official PSU | 1 | 5V/5A USB-C | Backup power |
| microSD Card | 1 | 16GB Class 10 | OS storage |
| GPIO Breakout | 1 | 40-pin | Safe GPIO access |
| Breadboard | 1 | 830 points | Prototyping |
| Jumper Wires | 1 set | 150pcs | Mixed M-M/M-F/F-F |
| Pushbutton | 1 | Tactile switch | Emergency shutdown |
| Playmobil House | 1 | | Enclosure |
| MDF Planks | 2 | 30x25x0.6cm | Base structure |
| Hinges | 2 | 25mm | Access doors |

## Power System
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| Solar Panel | 1 | 10W, 18V | Primary power source |
| Power Bank | 1 | 20,000mAh | Battery backup |
| DC-DC Converter | 1 | Step-down 5-24V→5V | Set to 5.1V output |

## Sensors
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| DS18B20 | 1 | Waterproof | Temperature |
| LDR | 1 | GL5528 | Light intensity |
| MFRC522 | 1 | RFID reader | With 2 cards |
| INA219 | 6 | I²C | Power monitoring |
| HC-SR501 | 1 | PIR | Motion detection |
| Reed Switch | 1 | NO | Door position |

## Interfaces
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| MCP3008 | 1 | 8-ch 10-bit ADC | Analog sensors |
| TCA9548A | 1 | 8-ch I²C Mux | INA219 expansion |

## Output Devices
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| 5mm LED | 6 | Red/Green/Yellow | Status indicators |
| Cooling Fan | 1 | 5V, 0.1A | Temperature control |
| Heating Pad | 1 | 5V, 2W | Anti-condensation |
| 16x2 LCD | 1 | I²C | System display |
| SG90 Servo | 1 | 180° rotation | Door lock |

## Electronic Components
| Component | Qty | Specs | Notes |
|-----------|-----|-------|-------|
| 10kΩ Pot | 2 | Linear | Manual controls |
| 4.7kΩ Res | 3 | 1/4W | Pull-up resistors |
| 470Ω Res | 3 | 1/4W | LED current limit |
| 100Ω Res | 6 | 1/4W | Transistor bases |
| 2kΩ Res | 3 | 1/4W | Signal conditioning |
| 1N5819 | 5 | Schottky | Protection diodes |
| 2N2222A | 3 | NPN | Heater drivers |
| SS8050 | 3 | NPN | Fan/LED drivers |

## Connectors & Accessories
| Component | Qty | Notes |
|-----------|-----|-------|
| Terminal Blocks | 10 | 2-5 pin |
| Heat Shrink | 1m | 3mm diameter |
| Cable Ties | 20 | 150mm |
| Solder | 1 | 60/40 Rosin core |

## Total Component Count: 58 items
> **Procurement Tip**: Order 10% extra resistors and diodes for prototyping losses
