from machine import ADC
import zcoap
import time
import ujson

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
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        reported['state']['reported']['battery'] = battery_voltage()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(60)

        cli.close()
