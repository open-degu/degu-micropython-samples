from machine import ADC
import zcoap
import time
import ujson

def battery_voltage():
    R6 = 68
    R8 = 100

    ain1 = ADC(1)
    raw = ain1.read()
    vin = (raw / 4096) * 0.6 * 6

    v = vin * ((R6 + R8) / R8)
    return v

if __name__ == '__main__':
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    while True:
        reported['state']['reported']['battery'] = battery_voltage()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(60)

    cli.close()
