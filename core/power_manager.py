import time

class PowerManager:
    def __init__(self, power_monitor):
        self.power_monitor = power_monitor
        self.solar_power = 0
        self.battery_level = 100  # Percentage
        self.last_update = time.time()
        
        # Power profiles
        self.power_modes = {
            "normal": {"fan": 100, "leds": 100, "heater": 100},
            "conserving": {"fan": 70, "leds": 50, "heater": 0},
            "critical": {"fan": 30, "leds": 10, "heater": 0}
        }

    def optimize_power(self):
        """Adjust system based on power availability"""
        # Get latest power data
        power_data = self.power_monitor.read_all()
        total_power = sum(item['power'] for item in power_data.values())
        
        # Update solar power (simple average)
        self.solar_power = (self.solar_power + total_power) / 2
        
        # Update battery level
        self._update_battery_level()
        
        # Determine power mode
        current_mode = self._determine_power_mode()
        
        return {
            "solar_power": self.solar_power,
            "battery_percent": self.battery_level,
            "power_mode": current_mode
        }

    def _update_battery_level(self):
        """Simulate battery state (would use actual measurements in real system)"""
        # Simple simulation: discharge 1% per hour when solar < 5W
        time_elapsed = time.time() - self.last_update
        discharge_rate = 1 / 3600  # 1% per hour
        
        if self.solar_power < 5:
            self.battery_level -= discharge_rate * time_elapsed
        elif self.solar_power > 10:
            self.battery_level += (discharge_rate * 2) * time_elapsed
        
        # Clamp between 0-100
        self.battery_level = max(0, min(100, self.battery_level))
        self.last_update = time.time()

    def _determine_power_mode(self):
        """Select appropriate power mode based on conditions"""
        if self.battery_level > 60 and self.solar_power > 15:
            return "normal"
        elif self.battery_level > 20:
            return "conserving"
        else:
            return "critical"
