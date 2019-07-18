from machine import Pin
from machine import Signal
import zcoap
import time
import ujson

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    sw4 = Pin(('GPIO_1', 14), Pin.IN, Pin.PULL_UP)
    terminal_d1 = Pin(('GPIO_1', 8), Pin.OUT)
    terminal_d2 = Pin(('GPIO_0', 7), Pin.OUT)

    before = 0
    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        value = sw4.value()
        if value != before:
            if value == 1:
                reported['state']['reported']['terminal'] = {'d1':'off', 'd2':'on'}
                terminal_d1.off()
                terminal_d2.on()
            else:
                reported['state']['reported']['terminal'] = {'d1':'on', 'd2':'off'}
                terminal_d1.on()
                terminal_d2.off()

            print(ujson.dumps(reported))
            cli.request_post(path, ujson.dumps(reported))
            before = value

        cli.close()
