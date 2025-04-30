import time
import math
import smbus

class PCA9685:
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        self.write(self.__MODE1, 0x00)

    def write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)
        if self.debug:
            print(f"I2C: Write 0x{value:02X} to register 0x{reg:02X}")

    def read(self, reg):
        value = self.bus.read_byte_data(self.address, reg)
        if self.debug:
            print(f"I2C: Read 0x{value:02X} from register 0x{reg:02X}")
        return value

    def set_pwm_freq(self, freq_hz):
        prescale = int(round(25000000.0 / 4096 / freq_hz - 1))
        old_mode = self.read(self.__MODE1)
        self.write(self.__MODE1, (old_mode & 0x7F) | 0x10)  # Sleep
        self.write(self.__PRESCALE, prescale)
        self.write(self.__MODE1, old_mode)
        time.sleep(0.005)
        self.write(self.__MODE1, old_mode | 0x80)

    def set_pwm(self, channel, on, off):
        reg = self.__LED0_ON_L + 4 * channel
        self.write(reg, on & 0xFF)
        self.write(reg + 1, on >> 8)
        self.write(reg + 2, off & 0xFF)
        self.write(reg + 3, off >> 8)

    def set_servo_angle(self, channel, angle, min_pulse=500, max_pulse=2500):
        pulse_range = max_pulse - min_pulse
        pulse = min_pulse + (pulse_range * (angle + 90) / 180)  # Shift -90 to 90 -> 0 to 180
        pwm_value = int(pulse * 4096 / 20000)  # Assuming 50Hz
        self.set_pwm(channel, 0, pwm_value)


def set_positions(pwm, x_angle, y_angles, x_min_pulse, x_max_pulse, y_min_pulse, y_max_pulse):
    pwm.set_servo_angle(0, x_angle, min_pulse=x_min_pulse, max_pulse=x_max_pulse)
    time.sleep(0.3)
    for y_angle in y_angles:
        pwm.set_servo_angle(1, y_angle, min_pulse=y_min_pulse, max_pulse=y_max_pulse)
        time.sleep(0.5)


if __name__ == '__main__':
    pwm = PCA9685(debug=False)
    pwm.set_pwm_freq(50)

    # Calibration settings for SG90
    x_min_pulse = 700
    x_max_pulse = 2000
    y_min_pulse = 1200
    y_max_pulse = 1700

    while True:
        # Left (-30)
        set_positions(pwm, -30, [-30, 0, 15], x_min_pulse, x_max_pulse, y_min_pulse, y_max_pulse)
        # Center (0)
        set_positions(pwm, 0, [-30, 0, 30], x_min_pulse, x_max_pulse, y_min_pulse, y_max_pulse)
        # Right (30)
        set_positions(pwm, 30, [-30, 0, 30], x_min_pulse, x_max_pulse, y_min_pulse, y_max_pulse)