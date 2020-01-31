from machine import ADC
from utime import sleep
import ujson
import degu
import math


class Temperature:
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

        self.thermistor = 3975

    def read_raw(self):
        value = self.adc.read()
        if value >= 32768:
            return 0
        else:
            return value

    def read(self):
        value = (self.read_raw() + 1) / 4
        resistance = (1023 - value) * 10000 / value
        return 1 / (math.log(resistance / 10000, 10) / self.thermistor + 1 / 298.15) - 273.15


def main():
    reported = {'state': {'reported': {}}}

    temperature = Temperature(0)

    while True:
        reported['state']['reported']['temperature'] = temperature.read()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(30)


if __name__ == "__main__":
    main()
