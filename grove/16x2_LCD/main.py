from machine import I2C
from time import sleep
import ujson
import degu


class LCD:
    def __init__(self):
        self.i2c = I2C(1)
        self.address = 0x3E
        self.write_command(0x3C)
        self.cls()

    def write_command(self, command):
        self.i2c.writeto(self.address, bytes([0x00, command & 0xFF]))

    def write_data(self, data):
        self.i2c.writeto(self.address, bytes([0x40, data & 0xFF]))

    def cls(self):
        commands = [0x0C, 0x01]

        for command in commands:
            self.write_command(command)
            sleep(0.01)

    def show_ascii(self, string):
        byte_string = bytearray(string)
        for char in byte_string:
            self.write_data(char)

    def newline(self):
        self.write_command(0xC0)
        sleep(0.01)


def main():
    def rotate_string(string, length):
        padded_string = (string + ' ' * length)[0:length]
        return padded_string[1:] + padded_string[0]

    def max(array):  # Micropython doesn't implement max()
        acc = array[0]
        for x in array[1:]:
            if acc < x:
                acc = x
        return acc

    lcd = LCD()

    string_top = 'Hello, world!'
    string_bottom = 'This is a grove LCD demo!'
    rotated_top = string_top
    rotated_bottom = string_bottom
    top_length = max([16, len(string_top)])
    bottom_length = max([16, len(string_bottom)])

    update_frequency = 10

    while True:
        shadow = ujson.loads(degu.get_shadow())
        if ('state' in shadow
           and 'reported' in shadow['state']
           and 'lcd' in shadow['state']['reported']):
            reported = shadow['state']['reported']['lcd']

            if ('string_top' in reported
               and reported['string_top'] != string_top):
                string_top = reported['string_top']
                rotated_top = string_top
                top_length = max([16, len(string_top)])

            if ('string_bottom' in reported
               and reported['string_bottom'] != string_bottom):
                string_bottom = reported['string_bottom']
                rotated_bottom = string_bottom
                bottom_length = max([16, len(string_bottom)])

        for i in range(update_frequency):
            lcd.cls()
            lcd.show_ascii(rotated_top[0:16])
            lcd.newline()
            lcd.show_ascii(rotated_bottom[0:16])

            if i != update_frequency - 1:  # Reduces the lag of transmission
                sleep(0.5)

            rotated_top = rotate_string(rotated_top, top_length + 1)
            rotated_bottom = rotate_string(rotated_bottom, bottom_length + 1)


if __name__ == '__main__':
    main()
