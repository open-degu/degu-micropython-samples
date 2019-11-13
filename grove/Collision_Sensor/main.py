from machine import Pin
from utime import sleep
import zcoap
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
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    collision = Collision(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['collision'] = collision.detect()
        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(1)
        cli.close()


if __name__ == "__main__":
    main()
