from machine import Pin
from machine import Signal
import zcoap
import time
import ujson

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    sw4 = Pin(('GPIO_1', 14), Pin.IN, Pin.PULL_UP)
    led = Pin(('GPIO_1', 8), Pin.OUT)

    before = 0
    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        value = sw4.value()
        if value != before:
            if value == 1:
                reported['state']['reported']['led'] = 'off'
                led.off()
            else:
                reported['state']['reported']['led'] = 'on'
                led.on()

            print(ujson.dumps(reported))
            cli.request_post(path, ujson.dumps(reported))
            before = value

        cli.close()
