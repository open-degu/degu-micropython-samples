from machine import ADC
from utime import sleep
import ujson
import degu


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
    reported = {'state': {'reported': {}}}

    loudness = Loudness(0)

    while True:
        reported['state']['reported']['loudness'] = loudness.read()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(30)


if __name__ == "__main__":
    main()
