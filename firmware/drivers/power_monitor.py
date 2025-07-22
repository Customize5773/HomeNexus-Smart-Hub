import smbus2
import time

class PowerMonitor:
    # INA219 Registers
    REG_CONFIG = 0x00
    REG_SHUNTVOLTAGE = 0x01
    REG_BUSVOLTAGE = 0x02
    REG_CURRENT = 0x04
    
    def __init__(self, mux_addr, addresses):
        self.bus = smbus2.SMBus(1)
        self.mux_addr = mux_addr
        self.addresses = addresses
        self.cal_values = {}
        
        # Initialize calibration for each sensor
        for addr in addresses:
            self._calibrate_sensor(addr)
    
    def _select_channel(self, channel):
        """Select I²C multiplexer channel (0-7)"""
        self.bus.write_byte(self.mux_addr, 1 << channel)
        time.sleep(0.01)
    
    def _calibrate_sensor(self, address):
        """Calculate calibration register value"""
        self._write_register(address, self.REG_CONFIG, 0x0000)  # Reset
        self._write_register(address, self.REG_CONFIG, 0x399F)  # 32V range, 1.9A max
        
        # Read calibration register
        config = self._read_register(address, self.REG_CONFIG)
        self.cal_values[address] = config
    
    def _read_register(self, address, register):
        data = self.bus.read_i2c_block_data(address, register, 2)
        return (data[0] << 8) | data[1]
    
    def _write_register(self, address, register, value):
        data = [(value >> 8) & 0xFF, value & 0xFF]
        self.bus.write_i2c_block_data(address, register, data)
    
    def read_sensor(self, address, channel):
        """Read power data from specific sensor"""
        self._select_channel(channel)
        
        shunt_voltage = self._read_register(address, self.REG_SHUNTVOLTAGE)
        bus_voltage = self._read_register(address, self.REG_BUSVOLTAGE)
        current = self._read_register(address, self.REG_CURRENT)
        
        # Convert to human-readable values
        return {
            'voltage': (bus_voltage >> 3) * 0.004,
            'current': current * 0.01,
            'power': (bus_voltage >> 3) * 0.004 * current * 0.01
        }
    
    def read_all(self):
        """Read all power sensors sequentially"""
        results = {}
        for i, addr in enumerate(self.addresses):
            results[f'ina219_{i}'] = self.read_sensor(addr, i)
        return results
