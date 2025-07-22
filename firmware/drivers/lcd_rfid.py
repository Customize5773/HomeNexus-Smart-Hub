import RPi.GPIO as GPIO
import smbus2
import time
import MFRC522

# LCD Constants
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
ENABLE = 0b00000100

class LCDController:
    def __init__(self, i2c_addr):
        self.addr = i2c_addr
        self.bus = smbus2.SMBus(1)
        self._init_lcd()
    
    def _init_lcd(self):
        # Initialization sequence
        self._lcd_byte(0x33, LCD_CMD)
        self._lcd_byte(0x32, LCD_CMD)
        self._lcd_byte(0x06, LCD_CMD)
        self._lcd_byte(0x0C, LCD_CMD)
        self._lcd_byte(0x28, LCD_CMD)
        self._lcd_byte(0x01, LCD_CMD)
        time.sleep(0.2)
    
    def _lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | 0x08
        bits_low = mode | ((bits << 4) & 0xF0) | 0x08
        
        # High nibble
        self.bus.write_byte(self.addr, bits_high)
        self._toggle_enable(bits_high)
        
        # Low nibble
        self.bus.write_byte(self.addr, bits_low)
        self._toggle_enable(bits_low)
    
    def _toggle_enable(self, bits):
        self.bus.write_byte(self.addr, (bits | ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.addr, (bits & ~ENABLE))
        time.sleep(0.0005)
    
    def show_message(self, text, line=1):
        text = text.ljust(LCD_WIDTH, " ")
        self._lcd_byte(LCD_LINE_1 if line == 1 else LCD_LINE_2, LCD_CMD)
        
        for char in text:
            self._lcd_byte(ord(char), LCD_CHR)
    
    def clear(self):
        self._lcd_byte(0x01, LCD_CMD)
        time.sleep(0.002)

class RFIDController:
    def __init__(self, rst_pin):
        self.reader = MFRC522.MFRC522()
        self.rst_pin = rst_pin
    
    def read_tag(self):
        (status, tag_type) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        
        if status == self.reader.MI_OK:
            (status, uid) = self.reader.MFRC522_Anticoll()
            
            if status == self.reader.MI_OK:
                return ':'.join([hex(x)[2:].upper() for x in uid])
        return None
