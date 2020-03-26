from machine import Pin
from utime import sleep
import degu
import ujson


class Magnetic:
    def __init__(self, port):
        pins = {
            0: ("GPIO_1",  8),
            1: ("GPIO_0",  6),
            2: ("GPIO_0", 12),
        }

        if port in pins.keys():
            self.pin = Pin(pins[port], Pin.IN)
        else:
            raise Exception("Port# out of range")

    def detect(self):
        return self.pin.value() == 1


def main():
    reported = {'state': {'reported': {}}}

    magnetic = Magnetic(0)

    while True:
        reported['state']['reported']['magnetic'] = magnetic.detect()
        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(1)


if __name__ == "__main__":
    main()
