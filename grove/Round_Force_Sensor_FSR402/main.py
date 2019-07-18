from machine import ADC
import zcoap
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
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}


    while True:
        addr = zcoap.gw_addr()
        port = 5683
        cli = zcoap.client((addr, port))

        force = round_force_sensor()
        reported['state']['reported']['force'] = force

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(1)

        cli.close()
