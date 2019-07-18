from machine import ADC
from utime import sleep
import ujson
import zcoap

class Loudness:
    def __init__(self, port):
        if port == 0:
            self.adc = ADC(0)
        elif port == 1:
            self.adc = ADC(4)
        elif port == 2:
            self.adc = ADC(6)
        else:
            raise Exception("Port# out of range")
    def read(self):
        valueSum = 0
        count = 0
        while count < 100:
            value = self.adc.read()
            if value < 4096 and value > 256:
                valueSum += value
                count += 1

        return valueSum / count

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    loudness = Loudness(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['loudness'] = loudness.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(1)
        cli.close()

if __name__ == "__main__":
    main()
