from machine import ADC
import degu
import time
import ujson

def d1_voltage():
    ADC_REF = 0.6
    ADC_RESOLUTION=4096 #12bit
    ain = ADC(0)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()
    v = (raw / ADC_RESOLUTION) * ADC_REF * 6
    return v

def d2_voltage():
    ADC_REF = 0.6
    ADC_RESOLUTION=4096 #12bit
    ain = ADC(5)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()
    v = (raw / ADC_RESOLUTION) * ADC_REF * 6
    return v

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    while True:
        d1 = round(d1_voltage(), 2)
        d2 = round(d2_voltage(), 2)
        reported['state']['reported']['terminal'] = {'d1':d1, 'd2':d2}

        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))
        time.sleep(1)
