from machine import ADC
import zcoap
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
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['angle'] = angle()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(1)

        cli.close()
