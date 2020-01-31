from machine import Pin
from utime import sleep
import degu
import ujson


class Collision:
    def __init__(self, port):
        pins = {
            0: (("GPIO_1",  8), ("GPIO_0",  7)),
            1: (("GPIO_0",  6), ("GPIO_0",  8)),
            2: (("GPIO_0", 12), ("GPIO_0", 14)),
        }

        if port in pins.keys():
            self.pins = [Pin(pin, Pin.IN) for pin in pins[port]]
        else:
            raise Exception("Port# out of range")

    def detect(self):
        return [pin.value() == 1 for pin in self.pins]


def main():
    reported = {'state': {'reported': {}}}

    collision = Collision(0)

    while True:
        reported['state']['reported']['collision'] = collision.detect()
        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(1)


if __name__ == "__main__":
    main()
