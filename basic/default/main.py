from machine import Pin
from machine import Signal
from machine import ADC
import degu
import time
import ujson

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    pin = Pin(('GPIO_1', 7), Pin.OUT)
    led1 = Signal(pin, invert=True)
    led1.off()

    while True:
        reported['state']['reported']['message'] = 'OK'
        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))

        received = degu.get_shadow()

        if received:
            led1.on()

        time.sleep(5)
