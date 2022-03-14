#!/usr/bin/env python

import SC16IS750
import SC16IS750_driver

class Serial (object):
    def __init__(self, privider: SC16IS750):
        self.privider = privider

    # def get_capacity(self):
        
    #     return min(capacity, 100)

if __name__=='__main__':

    # device = SC16IS750_driver.SC16IS750(0x4d)
    # # device.fPrintDebug()
    # if (not device.Connect(115200)):
    #     print("error SC16IS750_driver")

    device = SC16IS750.SC16IS750(14745000)
    device.setBaudrate(115200)
    # ups = Serial(device)
    print ("Test OK: " + str(device.testChip()))

    # while True:
    #     if (device.isDataWaiting()):
    #         print(chr(device.ReadByte()))