import time
import degu
import ujson
from machine import I2C

R_HIGH   = 1
R_MEDIUM = 2
R_LOW    = 3

class SHT31(object):
    _map_cs_r = {
        True: {
            R_HIGH : b'\x2c\x06',
            R_MEDIUM : b'\x2c\x0d',
            R_LOW: b'\x2c\x10'
            },
        False: {
            R_HIGH : b'\x24\x00',
            R_MEDIUM : b'\x24\x0b',
            R_LOW: b'\x24\x16'
            }
        }

    def __init__(self, i2c=None, addr=0x44):
        if i2c == None:
            raise ValueError('I2C object needed as argument!')
        self._i2c = i2c
        self._addr = addr

    def _send(self, buf):
        self._i2c.writeto(self._addr, buf)

    def _recv(self, count):
        return self._i2c.readfrom(self._addr, count)

    def _raw_temp_humi(self, r=R_HIGH, cs=True):
        if r not in (R_HIGH, R_MEDIUM, R_LOW):
            raise ValueError('Wrong repeatabillity value given!')
        self._send(self._map_cs_r[cs][r])
        time.sleep_ms(50)
        raw = self._recv(6)
        return (raw[0] << 8) + raw[1], (raw[3] << 8) + raw[4]

    def get_temp_humi(self, resolution=R_HIGH, clock_stretch=True, celsius=True):
        t, h = self._raw_temp_humi(resolution, clock_stretch)
        if celsius:
            temp = -45 + (175 * (t / 65535))
        else:
            temp = -49 + (315 * (t / 65535))
        return temp, 100 * (h / 65535)

def main():
    reported = {'state':{'reported':{}}}


    bus = I2C(1)
    sht31 = SHT31(i2c=bus)

    while True:
        values = sht31.get_temp_humi()

        reported['state']['reported']['temp'] = values[0]
        reported['state']['reported']['humid'] = values[1]

        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))
        time.sleep(60)

if __name__ == "__main__":
    main()
