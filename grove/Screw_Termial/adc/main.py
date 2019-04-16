from machine import ADC
import zcoap
import time
import ujson

def d1_voltage():
    ain1 = ADC(0)
    raw = ain1.read()
    v = (raw / 4096) * 0.6 * 6
    return v

def d2_voltage():
    ain1 = ADC(5)
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
        d1 = round(d1_voltage(), 2)
        d2 = round(d2_voltage(), 2)
        reported['state']['reported']['terminal'] = {'d1':d1, 'd2':d2}

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(1)

    cli.close()
