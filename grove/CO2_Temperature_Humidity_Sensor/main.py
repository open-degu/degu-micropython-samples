from machine import I2C
from time import sleep
import zcoap
import ujson
from ustruct import unpack


class CO2:
    def __init__(self):
        self.i2c = I2C(1)
        self.address = 0x61
        self.writeList([0x46, 0x00, 0x00, 0x02, 0x3D])
        self.writeList([0x00, 0x10, 0x00, 0x00, 0x81])
        sleep(3)

    def read(self, length):
        return self.i2c.readfrom(self.address, length)

    def writeList(self, data):
        self.i2c.writeto(self.address, bytes(data))

    def listToFloat(self, data):
        return unpack(">f", bytes(data))[0]

    def getConcentration(self):
        self.writeList([0x03, 0x00])
        buffer = self.read(18)
        co2 = self.listToFloat([buffer[0], buffer[1], buffer[3], buffer[4]])
        temperature = self.listToFloat([buffer[6], buffer[7], buffer[9], buffer[10]])
        humidity = self.listToFloat([buffer[12], buffer[13], buffer[15], buffer[16]])
        return [co2, temperature, humidity]


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        co2 = CO2()

        concentration = co2.getConcentration()
        reported['state']['reported']['co2'] = {
            'co2concentration': concentration[0],
            'temperature': concentration[1],
            'humidity': concentration[2]
        }

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(60)
        cli.close()


if __name__ == "__main__":
    main()
