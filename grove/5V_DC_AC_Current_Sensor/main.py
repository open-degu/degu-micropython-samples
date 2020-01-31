from machine import ADC
from time import sleep
import degu
import ujson

class Current:
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
        currentSum = 0
        for i in range(100):
            currentSum += (self.adc.read() * 3.3 / 4096 * 1000 - 1355) * 5
        return currentSum / 100

def main():
    reported = {'state':{'reported':{}}}


    current = Current(0)

    while True:
        reported['state']['reported']['current'] = current.read()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(1)

if __name__ == "__main__":
    main()
