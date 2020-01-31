from machine import Pin
import degu
import ujson

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    touch = Pin(('GPIO_1', 8), Pin.IN, Pin.PULL_UP)

    before = 0
    while True:
        value = touch.value()
        if value != before:
            if value == 0:
                reported['state']['reported']['touch'] = 'off'
            else:
                reported['state']['reported']['touch'] = 'on'

            print(ujson.dumps(reported))
            degu.update_shadow(ujson.dumps(reported))
            before = value
