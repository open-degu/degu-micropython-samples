from machine import Pin
from machine import Signal
from machine import ADC
import zcoap
import time
import ujson

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    pin = Pin(('GPIO_1', 7), Pin.OUT)
    led1 = Signal(pin, invert=True)
    led1.off()

    while True:
        reported['state']['reported']['message'] = 'OK'
        cli.request_post(path, ujson.dumps(reported))

        received = cli.request_get(path)

        if received:
            led1.on()

        time.sleep(5)

    cli.close()
