from machine import UART
import time
import zcoap
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

    def read(self, sentences):
        readdata = str(self.uart.readline(), 'ascii')
        for sentence in sentences:
            if sentence in readdata:
                if self.checksum_verify(readdata):
                    return readdata
        return None


class GPS_Parser:
    def __init__(self):
        self.datetime = ''
        self.lon = ''
        self.lat = ''
        self.pdop = ''

    def parse(self, nmea):
        parse_data = nmea.split(',')
        self.sentence_list[parse_data[0]](self, parse_data)
        return

    def change60to10(self, value):
        decimal, integer = math.modf(float(value) / 100.0)
        return str(integer + decimal / 60.0 * 100.0)

    def gprmc(self, parse_data):
        if parse_data[2] == 'A':
            time = str(int(parse_data[1][0:2]) + TIME_DIFF) + ':' + \
                           parse_data[1][2:4] + ':' + parse_data[1][4:6]
            date = parse_data[9][4:6] + '/' + parse_data[9][2:4] + \
                                        '/' + parse_data[9][0:2]
            self.datetime = date + ' ' + time
            self.lat = self.change60to10(parse_data[3]) + parse_data[4]
            self.lon = self.change60to10(parse_data[5]) + parse_data[6]
        else:
            self.datetime = ''
            self.lat = ''
            self.lon = ''
        return

    def gpgsa(self, parse_data):
        self.pdop = parse_data[15]
        return

    sentence_list = {'$GPRMC': gprmc, '$GPGSA': gpgsa}


def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state': {'reported': {}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    gps = GPS(0, GPS_BAUDRATE)
    parser = GPS_Parser()
    rcv_flag = {'GPRMC': 0, 'GPGSA': 0}

    while True:
        all_rcv = 0
        nmea = gps.read(("GPRMC", "GPGSA"))
        if nmea is None:
            pass
        else:
            parser.parse(nmea)
            for sentence in rcv_flag:
                if sentence in nmea:
                    rcv_flag[sentence] = 1
                all_rcv = all_rcv + rcv_flag[sentence]

            if all_rcv == len(rcv_flag):
                reported['state']['reported'] = {'datetime': parser.datetime,
                                                 'lat': parser.lat,
                                                 'lon': parser.lon,
                                                 'pdop': parser.pdop}
                json = ujson.dumps(reported)
                print(json)
                cli.request_post(path, json)
                for sentence in rcv_flag:
                    rcv_flag[sentence] = 0

        time.sleep_us(500)


if __name__ == "__main__":
    main()
