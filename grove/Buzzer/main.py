from machine import Pin
import degu
import ujson

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    sw4 = Pin(('GPIO_1', 14), Pin.IN, Pin.PULL_UP)
    buzzer = Pin(('GPIO_1', 8), Pin.OUT)

    before = 0
    while True:
        value = sw4.value()
        if value != before:
            if value == 1:
                reported['state']['reported']['buzzer'] = 'off'
                buzzer.off()
            else:
                reported['state']['reported']['buzzer'] = 'on'
                buzzer.on()

            print(ujson.dumps(reported))
            degu.update_shadow(ujson.dumps(reported))
            before = value
