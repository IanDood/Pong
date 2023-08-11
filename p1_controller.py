import smbus
import time

NUNCHUCK_DEVICE = 0x52

bus = smbus.SMBus(1)

def read_nunchuck_data():
    bus.write_byte_data(NUNCHUCK_DEVICE, 0x40, 0x00)
    time.sleep(0.1)

    bus.write_byte(NUNCHUCK_DEVICE, 0x00)
    time.sleep(0.1)

    bytes = [bus.read_byte(NUNCHUCK_DEVICE) for _ in range(6)]

    joyY = bytes[1]
    return joyY

try:
    while True:
        joyY = read_nunchuck_data()
        print("Joystick Y-axis value: {}".format(joyY))

except KeyboardInterrupt:
    print("Exiting the program.")
