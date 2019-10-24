from machine import Pin
from utime import sleep
import zcoap
import ujson


class PIR:
    def __init__(self, port):
        pins = {
            0: ("GPIO_1", 8),
            1: ("GPIO_0", 6),
            2: ("GPIO_0", 12),
        }

        if port in pins.keys():
            self.pin = Pin(pins[port], Pin.IN)
        else:
            raise Exception("Port# out of range")

    def detect(self):
        return self.pin.value() == 1


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    vib = PIR(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['motion'] = vib.detect()
        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(1)
        cli.close()


if __name__ == "__main__":
    main()
