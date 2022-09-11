
import math
import bluetooth as bt
import time

# parameters
DEBUG   = True
ALT_SPD = 114514


class vehicleCat:
    # This class is to define vehicle categories.
    # Default value of each vehicle should be 0.
    undefined = 0
    bike      = 1
    carSmall  = 2
    carBig    = 3


class vehicle:
    def __init__(self, ID=0, cat=0, dis=0xFFFF, ang=0xFFFF, spd=0, isAlt=False):
        self.name = ID
        self.cat  = cat
        self.xVal = ang * math.cos(ang)
        self.yVal = ang * math.sin(ang)
        self.dis  = dis
        self.spd  = spd
        self.alt  = isAlt


class vehicleControlPanel:
    def __init__(self):
        # dict format: {id(int):data(vehicle)}
        self.nowDict = dict()
        self.preDict = dict()
        self.nowTick = time.time()
        self.preTick = time.time()

    def update(self, data):
        self.preTick = self.nowTick
        self.nowTick = time.time()
        self.preDict = self.nowDict
        nowDictKeys  = self.nowDict.keys()
        self.nowDict.clear()
        try:
            for key in data:
                t = data[key]
                if key not in nowDictKeys:
                    self.nowDict[key] = vehicle(t.name, t.cat, t.dis, t.ang)
                else:
                    p  = self.preDict[key]
                    dy = p.yVal - (p.dis * math.sin(p.ang))
                    sp = dy / (self.nowTick - self.preTick)
                    self.nowDict[key] = vehicle(t.name, t.cat, t.dis, t.ang, sp, sp > ALT_SPD)
        except Exception as e:
            print("[VEHICLE CTRL] upd error:\r\n", e)


class commControlPanel:
    def __init__(self):
        self.disAddr = "C4:22:04:06:09:E5"
        self.disPort = 1
        self.bleSocket = bt.BluetoothSocket(bt.RFCOMM)
        self.windowPosNow    = 1
        self.windowSizeNow   = 1
        self.windowThreshold = 1
        self.windowRstCnt    = 0

    def packetSend(self, cont):
        contToSend = self.contEncode(cont)
        try:
            self.bleSocket.connect((self.disAddr, self.disPort))
            self.bleSocket.send(contToSend)
            if self.windowPosNow >= self.windowSizeNow:
                if self.windowSizeNow >= self.windowThreshold:
                    self.windowSizeNow += 1
                else:
                    self.windowSizeNow <<= 1
                self.windowPosNow = 0
                self.windowRstCnt = 0
                self.bleSocket.close()
            self.windowPosNow += 1
            # self.bleSocket.close()
            print("[COMM CTRL][PKT] PKT Send OK\r\n")
        except Exception as e:
            print("[COMM CTRL][PKT] socket error:\r\n", e)
            self.windowThreshold = self.windowSizeNow >> 1
            self.windowRstCnt += 1
            if self.windowRstCnt >= 3:
                self.windowSizeNow = 1
                self.windowRstCnt  = 0
            else:
                self.windowSizeNow = self.windowThreshold
            sock.close()

    @staticmethod
    def contEncode(cont):
        # cont is a dict from vehicleControlPanel
        ret = "-="
        ret += "tot:%d " % (len(cont))
        for key in cont:
            t = cont[key]
            ret += "%d,%d,%d,%d;" % (t.cat, t.xVal, t.yVal, t.alt)
        if DEBUG:
            print("[COMM CTRL][ENCODE] " + ret)
        return ret


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
