from machine import I2C
from time import sleep


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

    lcd = LCD()

    hello = 'Hello, world!'
    demo = 'This is a grove LCD demo!'
    demo_length = len(demo)

    while True:
        lcd.cls()
        lcd.show_ascii(hello)
        lcd.newline()
        lcd.show_ascii(demo[0:16])
        sleep(0.5)

        hello = rotate_string(hello, 16)
        demo = rotate_string(demo, demo_length + 2)


if __name__ == '__main__':
    main()
