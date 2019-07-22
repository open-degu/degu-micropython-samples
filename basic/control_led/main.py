import time
import zcoap
import ujson
from machine import Pin
from machine import Signal

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    pin = Pin(('GPIO_1', 5), Pin.OUT)
    led = Signal(pin, invert=True)
    led.off()
    led_status = 'OFF'

    while True:
        reported['state']['reported']['led'] = led_status

        cli.request_post(path, ujson.dumps(reported))

        received = cli.request_get(path)
        if received:
            try:
                desired = ujson.loads(received)
                try:
                    led_status = desired['state']['desired']['led']
                except:
                    pass
                if led_status == 'ON':
                    led.on()
                else:
                    led.off()
            except:
                pass

        time.sleep(1)

    cli.close()

if __name__ == "__main__":
    main()
