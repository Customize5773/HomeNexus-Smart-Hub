# Hardware Configuration
GPIO_CONFIG = {
    # Sensors
    "PIR_MOTION": 17,
    "REED_SWITCH": 27,
    "RFID_RST": 25,
    
    # Outputs
    "LEDS": [5, 6, 13, 19, 26, 21],
    "FAN": 20,
    "HEATER": 16,
    "SERVO": 12,
    
    # ADC (MCP3008)
    "ADC_CS": 8,
    "ADC_CLK": 11,
    "ADC_MISO": 9,
    "ADC_MOSI": 10,
    
    # I²C Addresses
    "I2C_MULTIPLEXER": 0x70,
    "LCD_DISPLAY": 0x27,
    "INA219_ADDRESSES": [0x40, 0x41, 0x42, 0x43, 0x44, 0x45]
}

# System Parameters
SYSTEM_SETTINGS = {
    "UPDATE_INTERVAL": 2.0,  # Seconds
    "TEMP_THRESHOLD": 25.0,  # °C
    "LIGHT_THRESHOLD": 300,  # LUX
    "ENERGY_LOG_INTERVAL": 300  # Seconds
}

# RFID Authorized Tags
AUTHORIZED_TAGS = [
    "5A:3B:7C:89",
    "B2:4F:61:9D"
]
