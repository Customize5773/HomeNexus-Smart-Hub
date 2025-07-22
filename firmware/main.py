import time
import json
from config import GPIO_CONFIG, SYSTEM_SETTINGS, AUTHORIZED_TAGS
from drivers.sensors import read_temperature, read_light_level, detect_motion
from drivers.power_monitor import PowerMonitor
from drivers.lcd_rfid import RFIDReader, LCDDisplay
from core.automation import AutomationEngine
from core.power_manager import PowerManager

# Initialize components
power_monitor = PowerMonitor(GPIO_CONFIG["I2C_MULTIPLEXER"], 
                            GPIO_CONFIG["INA219_ADDRESSES"])
rfid = RFIDReader(rst_pin=GPIO_CONFIG["RFID_RST"])
lcd = LCDDisplay(GPIO_CONFIG["LCD_DISPLAY"])
automation = AutomationEngine(GPIO_CONFIG)
power_manager = PowerManager(power_monitor)

def setup():
    """Initialize hardware interfaces"""
    print("Initializing HomeNexus system...")
    lcd.initialize()
    rfid.initialize()
    power_monitor.initialize()
    automation.initialize_outputs()
    lcd.show_message("System Ready")

def main_loop():
    """Primary control loop"""
    last_energy_log = time.time()
    
    while True:
        # Read sensor data
        temp = read_temperature()
        light = read_light_level(GPIO_CONFIG)
        motion = detect_motion(GPIO_CONFIG["PIR_MOTION"])
        
        # Check RFID access
        tag_id = rfid.read_tag()
        if tag_id:
            access = "GRANTED" if tag_id in AUTHORIZED_TAGS else "DENIED"
            lcd.show_message(f"Access {access}")
            automation.handle_access(tag_id in AUTHORIZED_TAGS)
        
        # Power management
        power_data = power_manager.optimize_power()
        
        # Execute automations
        automation.check_rules(temp, light, motion)
        
        # Periodic energy logging
        if time.time() - last_energy_log > SYSTEM_SETTINGS["ENERGY_LOG_INTERVAL"]:
            with open("energy_log.json", "a") as f:
                json.dump(power_data, f)
                f.write("\n")
            last_energy_log = time.time()
        
        # System status display
        lcd.show_status(temp, light, power_data["battery_percent"])
        time.sleep(SYSTEM_SETTINGS["UPDATE_INTERVAL"])

if __name__ == "__main__":
    try:
        setup()
        main_loop()
    except KeyboardInterrupt:
        print("System shutdown")
    finally:
        automation.cleanup()
        lcd.clear()
