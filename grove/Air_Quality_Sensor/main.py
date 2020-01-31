from machine import ADC
from time import sleep
import degu
import ujson

class AirQuality:
    def __init__(self, port):
        if port == 0:
            self.adc = ADC(0)
        elif port == 1:
            self.adc = ADC(4)
        elif port == 2:
            self.adc = ADC(6)
        else:
            raise Exception("Port# out of range")

    def read(self): #TODO: Not making sense as gas concentration
        return self.adc.read()
                
def main():
    reported = {'state':{'reported':{}}}


    air = AirQuality(0)

    while True:
        reported['state']['reported']['air_quality'] = air.read()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(60)

if __name__ == "__main__":
    main()
