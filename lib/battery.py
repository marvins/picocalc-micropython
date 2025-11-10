# battery.py - Battery monitoring for PicoCalc (Pico 2 with 2x 18650 parallel)
# 
# Hardware: 
# - 2x 18650 Li-ion batteries in parallel (7600mAh total)
# - VSYS ADC on Pico 2 (ADC pin 3)
# - Voltage range: 3.0V - 4.2V per cell
# - USB power detection: VSYS > 4.5V

from machine import ADC, Pin
import time

class BatteryMonitor:
    def __init__(self):
        # VSYS is connected to ADC3 on Pico/Pico2
        # VSYS has a voltage divider (typically 3:1)
        self.vsys_adc = ADC(29)  # GPIO29 is ADC3 (VSYS)
        
        # Li-ion voltage thresholds (per cell)
        self.VOLTAGE_MAX = 4.2  # Fully charged
        self.VOLTAGE_MIN = 3.0  # Critically low
        self.VOLTAGE_NOMINAL = 3.7  # Nominal voltage
        
        # USB detection threshold
        self.USB_THRESHOLD = 4.5  # VSYS > 4.5V means USB connected
        
        # ADC reference voltage (3.3V) and conversion factor
        self.ADC_VREF = 3.3
        self.ADC_MAX = 65535  # 16-bit ADC
        
        # VSYS voltage divider ratio (typically 3:1 on Pico)
        self.VSYS_DIVIDER = 3.0
        
    def read_vsys_voltage(self):
        """Read VSYS voltage in volts"""
        # Take multiple samples for stability
        samples = []
        for _ in range(10):
            raw = self.vsys_adc.read_u16()
            samples.append(raw)
            time.sleep_ms(1)
        
        # Average the samples
        avg_raw = sum(samples) // len(samples)
        
        # Convert to voltage
        # voltage = (raw / ADC_MAX) * VREF * DIVIDER_RATIO
        voltage = (avg_raw / self.ADC_MAX) * self.ADC_VREF * self.VSYS_DIVIDER
        
        return voltage
    
    def is_usb_powered(self, voltage=None):
        """Check if device is USB powered"""
        if voltage is None:
            voltage = self.read_vsys_voltage()
        return voltage > self.USB_THRESHOLD
    
    def voltage_to_percentage(self, voltage):
        """
        Convert battery voltage to percentage using a simplified Li-ion discharge curve
        
        Li-ion discharge curve (approximate):
        4.2V = 100%
        4.0V = 90%
        3.9V = 80%
        3.8V = 60%
        3.7V = 40%
        3.6V = 20%
        3.4V = 10%
        3.0V = 0%
        """
        # Voltage-to-percentage lookup table
        voltage_curve = [
            (4.20, 100),
            (4.10, 95),
            (4.00, 90),
            (3.90, 80),
            (3.80, 60),
            (3.70, 40),
            (3.60, 20),
            (3.40, 10),
            (3.20, 5),
            (3.00, 0),
        ]
        
        # If above max, return 100%
        if voltage >= voltage_curve[0][0]:
            return 100
        
        # If below min, return 0%
        if voltage <= voltage_curve[-1][0]:
            return 0
        
        # Linear interpolation between curve points
        for i in range(len(voltage_curve) - 1):
            v_high, p_high = voltage_curve[i]
            v_low, p_low = voltage_curve[i + 1]
            
            if voltage >= v_low:
                # Interpolate
                ratio = (voltage - v_low) / (v_high - v_low)
                percentage = p_low + ratio * (p_high - p_low)
                return int(percentage)
        
        return 0
    
    def get_status(self):
        """
        Get complete battery status
        
        Returns dict with:
        - voltage: Current VSYS voltage in volts
        - voltage_mv: Current VSYS voltage in millivolts
        - percentage: Battery charge percentage (0-100)
        - usb_power: True if USB powered
        - status: Text status ('Charging', 'Full', 'Discharging', 'Low', 'Critical')
        """
        voltage = self.read_vsys_voltage()
        usb_power = self.is_usb_powered(voltage)
        
        # If USB powered, don't calculate percentage (voltage is higher)
        if usb_power:
            percentage = None
            status = "USB Power"
        else:
            percentage = self.voltage_to_percentage(voltage)
            
            # Determine status based on percentage
            if percentage >= 90:
                status = "Full"
            elif percentage >= 20:
                status = "Good"
            elif percentage >= 10:
                status = "Low"
            else:
                status = "Critical"
        
        return {
            "voltage": round(voltage, 2),
            "voltage_mv": int(voltage * 1000),
            "percentage": percentage,
            "usb_power": usb_power,
            "status": status,
        }

# Global instance
_monitor = None

def get_monitor():
    """Get or create the global battery monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = BatteryMonitor()
    return _monitor

def get_status():
    """Convenience function to get battery status"""
    return get_monitor().get_status()

def get_percentage():
    """Convenience function to get battery percentage"""
    status = get_status()
    return status.get("percentage")

def get_voltage():
    """Convenience function to get battery voltage"""
    return get_monitor().read_vsys_voltage()
