from machine import ADC
from math import log
from utime import sleep
import ujson
import zcoap

class Temperature:
    def __init__(self, port):
        if port == 0:
            self.adc = ADC(5)
        elif port == 1:
            self.adc = ADC(7)
        elif port == 2:
            self.adc = ADC(3)
        else:
            raise Exception("Port# out of range")
        self.table = [
            [0, 2.5173462e1, -1.1662878, -1.0833638, -8.9773540/1e1, -3.7342377/1e1,
            -8.6632643/1e2, -1.0450598/1e2, -5.1920577/1e4],
            [0, 2.508355e1, 7.860106/1e2, -2.503131/1e1, 8.315270/1e2,
            -1.228034/1e2, 9.804036/1e4, -4.413030/1e5, 1.057734/1e6, -1.052755/1e8],
            [-1.318058e2, 4.830222e1, -1.646031, 5.464731/1e2, -9.650715/1e4,
            8.802193/1e6, -3.110810/1e8]
        ]
    def read(self):
        volSum = 0
        for i in range(20):
            volSum += self.adc.read()
        volSum /= 20
        vol = (float(int(volSum) >> 5) / 1023.0 * 5.0 * 1000.0 - 350.0) / 54.16
        kind = -1
        value = 0.0
        if vol >= -6.478 and vol < 0:
            kind = 0
            offset = 8
        elif vol >= 0 and vol < 20.644:
            kind = 1
            offset = 9
        elif vol >= 20.644 and vol <= 54.900:
            kind = 2
            offset = 6
        if kind != -1:
            value = self.table[kind][offset]
            while offset >= 0:
                offset -= 1
                value = vol * value + self.table[kind][offset]
        return value
         
def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    temp = Temperature(0)

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['temp'] = temp.read()

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(60)
        cli.close()

if __name__ == "__main__":
    main()
