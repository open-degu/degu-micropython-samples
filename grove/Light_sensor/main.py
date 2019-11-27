from machine import ADC
import degu
import time
import ujson

def light_sensor():
    ADC_REF = 0.6
    ADC_RESOLUTION=4096 #12bit
    ain = ADC(0)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()
    v = (raw / ADC_RESOLUTION) * ADC_REF * 6

    return v

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    while True:
        light = round(light_sensor(), 2)
        reported['state']['reported']['light'] = light

        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))
        time.sleep(1)
