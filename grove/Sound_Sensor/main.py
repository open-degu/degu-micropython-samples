from machine import ADC
from utime import sleep
import ujson
import zcoap


class Loudness:
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
        loudness = self.adc.read()
        if loudness >= 32768:
            return loudness - 65536
        else:
            return loudness


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    loudness = Loudness(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['loudness'] = loudness.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(30)
        cli.close()


if __name__ == "__main__":
    main()
