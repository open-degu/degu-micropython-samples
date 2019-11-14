from machine import ADC
from time import sleep
import zcoap
import ujson


class Current:
    def __init__(self, port):
        port_nums = [0, 4, 6]
        self.adc = ADC(port_nums[port])

    def read(self):
        return sum([(self.adc.read() - 285.5) / 0.9 for _ in range(100)]) / 100


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    current = Current(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['current'] = current.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(1)
        cli.close()


if __name__ == "__main__":
    main()
