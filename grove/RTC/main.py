from machine import I2C
from time import sleep
import degu
import ujson


class RTC:
    def __init__(self):
        self.i2c = I2C(1)
        self.address = 0x68

    def decToBcd(self, value):
        return (value // 10 * 16 + value % 10) & 0xFF

    def bcdToDec(self, value):
        return (value // 16 * 10) + value % 16

    def dayOfWeek(self, year, month, day):
        if month <= 2:
            month += 12
            year -= 1
        return (
                day + 5 +
                int(26 * (month + 1) / 10) +
                year % 100 + int (year % 100 / 4) +
                -2 * int(year / 100) +
                int(int(year / 100) / 4)
            ) % 7 + 1

    def read(self, length):
        return self.i2c.readfrom(self.address, length)

    def writeList(self, data):
        self.i2c.writeto(self.address, bytes(data))

    def setTime(self, year, month, day, hour, minute, second):
        dayOfWeek = self.dayOfWeek(year, month, day)
        self.writeList(map(self.decToBcd, [0x00, second, minute, hour, dayOfWeek, day, month, year - 2000]))

    def getTime(self):
        self.writeList([0x00])
        time = self.read(7)
        second = self.bcdToDec(time[0] & 0x7F)
        minute = self.bcdToDec(time[1])
        hour = self.bcdToDec(time[2] & 0x3F)
        dayOfWeek = self.bcdToDec(time[3]) - 1
        day = self.bcdToDec(time[4])
        month = self.bcdToDec(time[5])
        year = self.bcdToDec(time[6])
        return [2000 + year, month, day, dayOfWeek, hour, minute, second]

def main():
    reported = {'state':{'reported':{}}}


    rtc = RTC()

    # RTC initialization
    rtc.setTime(2019, 5, 22, 17, 31, 30)

    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    formatString = "{}-{:0>2}-{:0>2}({:0>2}) {:0>2}:{:0>2}:{:0>2}"

    while True:
        time = rtc.getTime()
        reported['state']['reported']['time'] = {"time": formatString.format(
            time[0], time[1], time[2], days[time[3]], time[4], time[5], time[6]
        )}

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)
        sleep(1)


if __name__ == "__main__":
    main() 
