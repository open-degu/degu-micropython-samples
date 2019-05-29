from machine import I2C
from time import sleep
import zcoap
import ujson
from ustruct import unpack

class PM25:
    def __init__(self):
        self.i2c = I2C(1)
        self.address = 0x40

    def read(self, length):
        return self.i2c.readfrom(self.address, length)

    def getConcentration(self):
        data = self.read(16)
        result = []
        for i in range(6):
            result.append(unpack(">H", data[(i + 2) * 2: (i + 3) * 2])[0])
        return result
                
def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    pm25 = PM25()

    while True:
        concentration = pm25.getConcentration()
        reported['state']['reported']['pollution'] = {
            'pm1.0': concentration[0],
            'pm2.5': concentration[1],
            'pm10': concentration[2]
        }

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(60)

if __name__ == "__main__":
    main()