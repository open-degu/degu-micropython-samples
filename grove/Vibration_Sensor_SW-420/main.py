from machine import Pin
from utime import ticks_ms, sleep
import zcoap
import ujson

class Vibration:
    def __init__(self, port, interval = 100):
        if port == 0:
            self.pin = Pin(("GPIO_1", 8), Pin.IN)
        elif port == 1:
            self.pin = Pin(("GPIO_0", 6), Pin.IN)
        elif port == 2:
            self.pin = Pin(("GPIO_0", 12), Pin.IN)
        else:
            raise Exception("Port# out of range")
        self.prev = 0
        self.interval = interval

    def detect(self):
        result = False
        current = ticks_ms()
        if self.pin.value() == 0:
            if current - self.prev > self.interval:
                result = True
            self.prev = current
        return result

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    vib = Vibration(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['vibration'] = "not detected"
        for i in range(100):
            if vib.detect():
                reported['state']['reported']['detected'] = "detected"
            sleep(0.01)
        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        cli.close()

if __name__ == "__main__":
    main()
