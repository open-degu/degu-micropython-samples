from machine import ADC
import degu
import time
import ujson

def round_force_sensor():
    ain = ADC(0)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()

    if raw > 60000 :
        raw = 0

    return raw

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    while True:
        force = round_force_sensor()
        reported['state']['reported']['force'] = force

        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))
        time.sleep(1)
