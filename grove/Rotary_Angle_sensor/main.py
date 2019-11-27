from machine import ADC
import degu
import time
import ujson

def angle():
    ANGLE_FULL = 300 # 300 degrees
    ADC_RAW_MAX = 3740
    ain = ADC(0)
    ain.gain(ain.GAIN_1_6) #gain set to 1/6

    raw = ain.read()
    if raw > 60000:
        raw = 0

    degrees = (raw / ADC_RAW_MAX) * ANGLE_FULL

    return round(degrees)

if __name__ == '__main__':
    reported = {'state':{'reported':{}}}


    while True:
        reported['state']['reported']['angle'] = angle()

        print(ujson.dumps(reported))
        degu.update_shadow(ujson.dumps(reported))
        time.sleep(1)
