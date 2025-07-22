import RPi.GPIO as GPIO
import time

class AutomationEngine:
    def __init__(self, config):
        self.config = config
        self.led_pins = config["LEDS"]
        self.fan_pin = config["FAN"]
        self.heater_pin = config["HEATER"]
        self.servo_pin = config["SERVO"]
        self.door_pin = config["REED_SWITCH"]
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        GPIO.setup(self.heater_pin, GPIO.OUT)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        GPIO.setup(self.door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Initialize PWM for servo and fan
        self.servo_pwm = GPIO.PWM(self.servo_pin, 50)  # 50Hz servo
        self.fan_pwm = GPIO.PWM(self.fan_pin, 1000)    # 1kHz fan
        self.servo_pwm.start(0)
        self.fan_pwm.start(0)
        
        # State tracking
        self.door_open = False
        self.last_motion_time = 0
        self.lighting_mode = "auto"  # auto/manual/off

    def initialize_outputs(self):
        """Set all outputs to safe initial state"""
        for pin in self.led_pins:
            GPIO.output(pin, GPIO.LOW)
        self.fan_pwm.ChangeDutyCycle(0)
        GPIO.output(self.heater_pin, GPIO.LOW)
        self.servo_pwm.ChangeDutyCycle(0)

    def check_rules(self, temperature, light_level, motion_detected):
        """Evaluate all automation rules"""
        self._temperature_rules(temperature)
        self._lighting_rules(light_level, motion_detected)
        self._security_rules(motion_detected)
        
        # Update motion timestamp
        if motion_detected:
            self.last_motion_time = time.time()

    def handle_access(self, authorized):
        """Handle RFID access events"""
        if authorized:
            self._unlock_door()
            time.sleep(5)  # Keep door unlocked
            self._lock_door()
        else:
            self._trigger_alarm()

    def _temperature_rules(self, temperature):
        """Temperature-based automations"""
        threshold = self.config["TEMP_THRESHOLD"]
        
        # Cooling fan control
        if temperature > threshold + 2:
            self.fan_pwm.ChangeDutyCycle(100)
        elif temperature > threshold:
            self.fan_pwm.ChangeDutyCycle(50)
        else:
            self.fan_pwm.ChangeDutyCycle(0)
            
        # Heater control (with hysteresis)
        if temperature < threshold - 3:
            GPIO.output(self.heater_pin, GPIO.HIGH)
        elif temperature > threshold - 1:
            GPIO.output(self.heater_pin, GPIO.LOW)

    def _lighting_rules(self, light_level, motion_detected):
        """Lighting automation based on ambient light and motion"""
        # Manual override modes
        if self.lighting_mode == "off":
            self._set_leds(0)
            return
        elif self.lighting_mode == "manual":
            self._set_leds(50)  # Medium brightness
            return
            
        # Auto mode rules
        motion_timeout = 300  # 5 minutes
        
        if light_level < self.config["LIGHT_THRESHOLD"]:
            if motion_detected:
                self._set_leds(100)  # Full brightness
            elif time.time() - self.last_motion_time < motion_timeout:
                self._set_leds(30)  # Low brightness
            else:
                self._set_leds(0)   # Lights off
        else:
            self._set_leds(0)  # Enough ambient light

    def _security_rules(self, motion_detected):
        """Security-related automations"""
        # Door status monitoring
        door_open = GPIO.input(self.door_pin) == GPIO.HIGH
        
        if door_open and not self.door_open:
            print("Door opened!")
            # Add notification here
            
        self.door_open = door_open
        
        # Intrusion detection (motion when away)
        # Add logic based on system armed state

    def _set_leds(self, brightness):
        """Control all LEDs with PWM brightness (0-100)"""
        for pin in self.led_pins:
            if brightness > 0:
                pwm = GPIO.PWM(pin, 1000)
                pwm.start(brightness)
            else:
                GPIO.output(pin, GPIO.LOW)

    def _lock_door(self):
        """Lock door using servo"""
        self.servo_pwm.ChangeDutyCycle(7.5)  # 90 degrees position
        time.sleep(0.5)
        self.servo_pwm.ChangeDutyCycle(0)

    def _unlock_door(self):
        """Unlock door using servo"""
        self.servo_pwm.ChangeDutyCycle(2.5)  # 0 degrees position
        time.sleep(0.5)
        self.servo_pwm.ChangeDutyCycle(0)

    def _trigger_alarm(self):
        """Visual alarm for unauthorized access"""
        for _ in range(5):
            self._set_leds(100)
            time.sleep(0.2)
            self._set_leds(0)
            time.sleep(0.2)

    def cleanup(self):
        """Clean up resources"""
        self.fan_pwm.stop()
        self.servo_pwm.stop()
        GPIO.cleanup()
