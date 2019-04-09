import machine
import micropython
import zcoap
import ujson
import time

message = 'OK'
path = 'thing/' + zcoap.eui64()
reported = ujson.dumps({'state':{ 'reported':{ 'message':message } } })

pin = machine.Pin(('GPIO_1', 7), machine.Pin.OUT)
led1 = machine.Signal(pin, invert=True)
led1.off()

addr = zcoap.gw_addr()
port = 5683
cli = zcoap.client((addr, port))

while True:
    cli.request_post(path, reported)
    received = cli.request_get(path)

    if received:
        led1.on()

    time.sleep(5)

cli.close()
