import machine
import time
import degu

if __name__ == '__main__':
    while True:
        print("Hello! I'm Alice.")
        if (degu.check_update()):
            print("New script is comming! Restarting...")
            machine.reset();

        time.sleep(1)
