from machine import I2C
from time import sleep
import zcoap
import ujson

class ColorSensor:
    def __init__(self):
        self.i2c = I2C(1)
        self.address = 0x29
        self.initialized = False

    def writeList(self, data):
        self.i2c.writeto(self.address, bytes(data))

    def write(self, register, data):
        if type(data) is not list:
            return

        self.writeList([(register | 0x80) & 0xFF] + data)

    def read(self, register, length):
        self.writeList([(register | 0x80) & 0xFF])
        response = self.i2c.readfrom(self.address, length + 10)

        result = 0
        for i in range(length):
            result += int(response[i]) * (256 ** i)
        return result

    def begin(self):
        response = self.read(0x12, 1)
        if response != 0x44 and response != 0x10:
            return False
        self.initialized = True
        self.write(0x01, [0xEB])
        self.write(0x0F, [0x01])
        self.write(0x00, [0x01])
        sleep(0.01)
        self.write(0x00, [0x03])
        return True

    def readColor(self):
        if not self.initialized:
            if self.begin() == False:
                return [0, 0, 0, 0]

        sleep(0.05)

        clear = self.read(0x14, 2) + 1
        red = self.read(0x16, 2) / clear * 256
        green = self.read(0x18, 2) / clear * 256
        blue = self.read(0x1A, 2) / clear * 256

        return [red, green, blue]

                
def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    colorSensor = ColorSensor()

    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        color = colorSensor.readColor()
        reported['state']['reported']['color'] = {
            'red': color[0],
            'green': color[1],
            'blue': color[2]
        }

        json = ujson.dumps(reported)
        cli.request_post(path, json)
        print(json)
        sleep(60)
        cli.close()

if __name__ == "__main__":
    main()
