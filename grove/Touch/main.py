from machine import Pin
from machine import Signal
import zcoap
import time
import ujson

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    touch = Pin(('GPIO_1', 8), Pin.IN, Pin.PULL_UP)

    before = 0
    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        value = touch.value()
        if value != before:
            if value == 0:
                reported['state']['reported']['touch'] = 'off'
            else:
                reported['state']['reported']['touch'] = 'on'

            print(ujson.dumps(reported))
            cli.request_post(path, ujson.dumps(reported))
            before = value

        cli.close()
