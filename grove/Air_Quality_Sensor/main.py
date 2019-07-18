from machine import ADC
from time import sleep
import zcoap
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
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    air = AirQuality(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['air_quality'] = air.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(60)
        cli.close()

if __name__ == "__main__":
    main()
