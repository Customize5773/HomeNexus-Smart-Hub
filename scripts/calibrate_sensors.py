#!/usr/bin/env python3
# HomeNexus Sensor Calibration Utility
# Usage: python calibrate_sensors.py [sensor-type]

import time
import sys
import json
import RPi.GPIO as GPIO
from datetime import datetime
from drivers.sensors import TemperatureSensor, LightSensor, MotionSensor, DoorSensor
from drivers.power_monitor import PowerMonitor
from drivers.lcd_rfid import LCDController
from config import GPIO_CONFIG

# Initialize LCD
lcd = LCDController(GPIO_CONFIG["LCD_DISPLAY"])

def calibrate_temperature():
    """Calibrate DS18B20 against known temperatures"""
    print("Temperature Calibration")
    print("Place sensor in known temperature environments")
    lcd.show_message("Temp Cal: Ice Bath")
    
    samples = []
    print("1. Ice Bath (0°C) - Place sensor in ice water")
    input("Press Enter when ready...")
    for _ in range(10):
        samples.append(TemperatureSensor().read())
        time.sleep(1)
    ice_avg = sum(samples) / len(samples)
    
    samples = []
    print("\n2. Room Temperature - Leave sensor in air")
    input("Press Enter when ready...")
    for _ in range(10):
        samples.append(TemperatureSensor().read())
        time.sleep(1)
    room_avg = sum(samples) / len(samples)
    
    # Calculate calibration factors
    offset = room_avg - 25  # Assuming 25°C room temp
    gain = (room_avg - ice_avg) / 25
    
    print(f"\nCalibration Results:")
    print(f"Offset: {offset:.2f}°C")
    print(f"Gain: {gain:.2f} (ideal=1.0)")
    
    return {
        "sensor": "DS18B20",
        "offset": offset,
        "gain": gain,
        "timestamp": str(datetime.now())
    }

def calibrate_light():
    """Calibrate LDR against lux meter"""
    print("\nLight Sensor Calibration")
    print("Use lux meter for reference values")
    lcd.show_message("Light Cal: Dark")
    
    # Dark calibration
    input("Cover sensor completely (0 lux), then press Enter...")
    dark_value = LightSensor(
        GPIO_CONFIG["ADC_CLK"],
        GPIO_CONFIG["ADC_CS"],
        GPIO_CONFIG["ADC_MISO"],
        GPIO_CONFIG["ADC_MOSI"]
    ).read_lux()
    
    # Bright calibration
    lcd.show_message("Light Cal: Bright")
    lux = float(input("Point sensor at bright light, enter lux meter value: "))
    bright_value = LightSensor(
        GPIO_CONFIG["ADC_CLK"],
        GPIO_CONFIG["ADC_CS"],
        GPIO_CONFIG["ADC_MISO"],
        GPIO_CONFIG["ADC_MOSI"]
    ).read_lux()
    
    # Calculate scaling factor
    scale = lux / (bright_value - dark_value)
    
    print(f"\nCalibration Results:")
    print(f"Dark Value: {dark_value}")
    print(f"Bright Value: {bright_value}")
    print(f"Scaling Factor: {scale:.2f}")
    
    return {
        "sensor": "LDR",
        "dark_value": dark_value,
        "scale_factor": scale,
        "timestamp": str(datetime.now())
    }

def calibrate_rfid():
    """Register authorized RFID tags"""
    print("\nRFID Tag Registration")
    print("Scan tags to authorize (Ctrl+C to stop)")
    lcd.show_message("RFID Cal: Scan Tags")
    
    from drivers.lcd_rfid import RFIDController
    rfid = RFIDController(GPIO_CONFIG["RFID_RST"])
    tags = []
    
    try:
        while True:
            print("Waiting for tag...")
            tag_id = rfid.read_tag()
            if tag_id:
                print(f"Detected: {tag_id}")
                if tag_id not in tags:
                    tags.append(tag_id)
                    print(f"Added to authorized list")
                    lcd.show_message(f"Added: {tag_id[:6]}", 2)
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nRegistration complete")
    
    return {
        "sensor": "RFID",
        "authorized_tags": tags,
        "timestamp": str(datetime.now())
    }

def calibrate_power():
    """Calibrate INA219 power sensors"""
    print("\nPower Sensor Calibration")
    print("Apply known loads to each channel")
    lcd.show_message("Power Cal: Start")
    
    monitor = PowerMonitor(
        GPIO_CONFIG["I2C_MULTIPLEXER"],
        GPIO_CONFIG["INA219_ADDRESSES"]
    )
    results = {}
    
    for i, addr in enumerate(GPIO_CONFIG["INA219_ADDRESSES"]):
        lcd.show_message(f"INA219 #{i+1}", 1)
        lcd.show_message("Apply load >1W", 2)
        
        input(f"\nConnect load to INA219 #{i+1} (address {hex(addr)}), then press Enter...")
        readings = []
        for _ in range(5):
            data = monitor.read_sensor(addr, i)
            readings.append(data)
            print(f"Reading: {data}")
            time.sleep(1)
        
        # Get reference values
        ref_voltage = float(input("Enter multimeter voltage (V): "))
        ref_current = float(input("Enter reference current (A): "))
        
        # Calculate calibration factors
        avg_voltage = sum(r['voltage'] for r in readings) / len(readings)
        avg_current = sum(r['current'] for r in readings) / len(readings)
        
        voltage_factor = ref_voltage / avg_voltage if avg_voltage else 1.0
        current_factor = ref_current / avg_current if avg_current else 1.0
        
        results[f"ina219_{i}"] = {
            "address": addr,
            "voltage_factor": voltage_factor,
            "current_factor": current_factor,
            "ref_voltage": ref_voltage,
            "ref_current": ref_current
        }
    
    return {
        "sensor": "INA219",
        "calibrations": results,
        "timestamp": str(datetime.now())
    }

def save_calibration(data):
    """Save calibration data to file"""
    filename = f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nCalibration saved to {filename}")
    lcd.show_message("Calibration Saved!", 1)
    lcd.show_message(filename, 2)

if __name__ == "__main__":
    try:
        sensor_type = sys.argv[1] if len(sys.argv) > 1 else "all"
        
        cal_data = {}
        
        if sensor_type in ["temp", "all"]:
            cal_data["temperature"] = calibrate_temperature()
        
        if sensor_type in ["light", "all"]:
            cal_data["light"] = calibrate_light()
        
        if sensor_type in ["rfid", "all"]:
            cal_data["rfid"] = calibrate_rfid()
        
        if sensor_type in ["power", "all"]:
            cal_data["power"] = calibrate_power()
        
        save_calibration(cal_data)
        
    except Exception as e:
        print(f"Calibration failed: {str(e)}")
        lcd.show_message("Error!", 1)
        lcd.show_message(str(e)[:16], 2)
    finally:
        GPIO.cleanup()
