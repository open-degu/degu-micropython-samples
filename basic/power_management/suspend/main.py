from machine import ADC
import ujson

import degu

def battery_voltage():
    R6 = 68
    R8 = 100

    ADC_REF = 0.6
    ADC_RESOLUTION=4096 #12bit
    ain = ADC(1)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()
    vin = (raw / ADC_RESOLUTION) * ADC_REF * 6

    v = vin * ((R6 + R8) / R8)
    return v

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}

    while True:
        reported['state']['reported']['battery'] = battery_voltage()

        json = ujson.dumps(reported)
        degu.update_shadow(json)
        print(json)

        degu.suspend(30)
