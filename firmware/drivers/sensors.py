import os
import glob
import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008 as MCP

# Configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class TemperatureSensor:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.device_file = glob.glob('/sys/bus/w1/devices/28*')[0] + '/w1_slave'
    
    def read_raw(self):
        with open(self.device_file, 'r') as f:
            return f.readlines()
    
    def read(self):
        lines = self.read_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_raw()
        
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_str = lines[1][equals_pos+2:]
            return float(temp_str) / 1000.0

class LightSensor:
    def __init__(self, clk, cs, miso, mosi, channel=0):
        self.adc = MCP.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
        self.channel = channel
    
    def read_lux(self):
        # Returns approximate lux value (0-1000)
        raw_value = self.adc.read_adc(self.channel)
        return int(raw_value / 10.23)  # Convert 10-bit ADC to lux %

class MotionSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)
    
    def detect(self):
        return GPIO.input(self.pin)

class DoorSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def is_open(self):
        return GPIO.input(self.pin) == GPIO.HIGH
