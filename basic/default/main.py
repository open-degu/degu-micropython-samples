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
        degu.request_post(ujson.dumps(reported))

        received = degu.request_get()

        if received:
            led1.on()

        time.sleep(5)
