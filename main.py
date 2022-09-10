import bluetooth as bt
import time

disAddr = "C4:22:04:06:09:E5"

print("Hello World")

nearby_devices = bt.discover_devices(5, flush_cache=True, lookup_names=True)

print("Found {} devices.".format(len(nearby_devices)))

print(nearby_devices)

sock = bt.BluetoothSocket(bt.RFCOMM)


def sendQwQtoDis():
    port = 1

    try:
        print("connect to dis")
        sock.connect((disAddr, port))
        sock.send("QwQ")
        sock.close()

    except Exception as e:
        print("[SOCKET ERROR] ", e)


while True:
    sendQwQtoDis()
    time.sleep(1)

