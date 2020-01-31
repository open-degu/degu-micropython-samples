from machine import ADC
from time import sleep
import degu
import ujson


class Current:
    def __init__(self, port):
        port_nums = [0, 4, 6]
        self.adc = ADC(port_nums[port])

    def read(self):
        return sum([(self.adc.read() - 285.5) / 0.9 for _ in range(100)]) / 100


def main():
    reported = {'state': {'reported': {}}}

    current = Current(0)

    while True:
        reported['state']['reported']['current'] = current.read()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(1)


if __name__ == "__main__":
    main()
