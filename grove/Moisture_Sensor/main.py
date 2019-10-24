from machine import ADC
from utime import sleep
import ujson
import zcoap


class Moisture:
    def __init__(self, port):
        ports = {
            0: 0,
            1: 4,
            2: 6
        }

        if port in ports.keys():
            self.adc = ADC(ports[port])
        else:
            raise Exception("Port# out of range")

    def read(self):
        moisture = self.adc.read()
        if moisture >= 32768:
            return moisture - 65536
        else:
            return moisture


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    moisture = Moisture(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['moisture'] = moisture.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(30)
        cli.close()


if __name__ == "__main__":
    main()
