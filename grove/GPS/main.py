from machine import UART
import time
import degu
import ujson
import math

GPS_BAUDRATE = 9600
TIME_DIFF = 9


class GPS:
    def __init__(self, id, baud):
        if id == 0:
            self.uart = UART(id, baud)
        else:
            raise Exception("Port# out of range")

    def checksum_verify(self, nmea):
        calc = 0
        checksum = int(nmea[-4:-2], 16)
        for c in nmea:
            if c == '$':
                pass
            elif c == '*':
                break
            else:
                calc = calc ^ int(hex(ord(c)), 16)
        if calc == checksum:
            return True
        else:
            return False

    def rcv_verify(self, data, sentences):
        for sentence in sentences:
            if sentence not in data:
                return False
        return True

    def parse(self, nmea, sentence):
        parse_data = nmea.split(',')
        func = getattr(self, sentence)
        return func(parse_data)

    def change60to10(self, value):
        decimal, integer = math.modf(float(value) / 100.0)
        return str(integer + decimal / 60.0 * 100.0)

    def gprmc(self, parse_data):
        if parse_data[2] == 'A':
            time = str(int(parse_data[1][0:2]) + TIME_DIFF) + ':' + \
                           parse_data[1][2:4] + ':' + parse_data[1][4:6]
            date = parse_data[9][4:6] + '/' + parse_data[9][2:4] + \
                                        '/' + parse_data[9][0:2]
            datetime = date + ' ' + time
            lat = self.change60to10(parse_data[3]) + parse_data[4]
            lon = self.change60to10(parse_data[5]) + parse_data[6]
        else:
            datetime = ''
            lat = ''
            lon = ''
        return {'lat': lat, 'lon': lon, 'datetime': datetime}

    def gpgsa(self, parse_data):
        return {'pdop': parse_data[15]}

    def read(self, sentences):
        parsedata = {}
        # Clear all buffers
        buf = self.uart.read(self.uart.any())
        while True:
            readdata = str(self.uart.readline(), 'ascii')
            for sentence in sentences:
                if sentence in readdata.lower():
                    if self.checksum_verify(readdata):
                        parsedata[sentence] = {}
                        parsedata[sentence] = self.parse(readdata, sentence)
                        break
            if self.rcv_verify(parsedata, sentences):
                return parsedata


def main():
    reported = {'state': {'reported': {}}}


    gps = GPS(0, GPS_BAUDRATE)

    while True:
        reported['state']['reported'] = gps.read(("gprmc", "gpgsa"))
        json = ujson.dumps(reported)
        print(json)
        degu.update_shadow(json)
        time.sleep(1)


if __name__ == "__main__":
    main()
