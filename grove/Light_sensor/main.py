from machine import ADC
import zcoap
import time
import ujson

def light_sensor():
    ain1 = ADC(0)
    raw = ain1.read()
    v = (raw / 4096) * 0.6 * 6
    return v

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    while True:
        light = round(light_sensor(), 2)
        reported['state']['reported']['light'] = light

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(1)

    cli.close()
