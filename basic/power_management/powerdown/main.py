import time
import ujson

import degu

def update_power_state(state):
    reported = {'state':{'reported':{}}}
    reported['state']['reported']['state'] = state

    json = ujson.dumps(reported)
    degu.update_shadow(json)
    print(json)

if __name__ == '__main__':
    update_power_state('wakeup')

    print("power down after 15 seconds...")
    time.sleep(15)

    update_power_state('powerdown')
    degu.powerdown()
