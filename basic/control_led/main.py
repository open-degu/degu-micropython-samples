import time
import degu
import ujson
from machine import Pin
from machine import Signal

def main():
    pin = Pin(('GPIO_1', 5), Pin.OUT)
    led = Signal(pin, invert=True)
    led.off()
    led_status = 'OFF'

    while True:
        reported = {'state': {'reported': {}}}

        reported['state']['reported']['led'] = led_status

        degu.request_post(ujson.dumps(reported))

        received = degu.update_shadow()
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

if __name__ == "__main__":
    main()
