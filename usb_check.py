#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import usb

busses = usb.busses()

for bus in busses:
    devices = bus.devices
    for dev in devices:
        handle = dev.open()
        print("Device:", dev.filename)
        print("  VID: 0x{:04x}".format(dev.idVendor))
        print("  PID: 0x{:04x}".format(dev.idProduct))
        print("  Manufacturer: 0x{:x}".format(dev.iManufacturer), end='')

'''
import re
import subprocess
device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []
for i in df.split('\n'):
    if i:
        info = device_re.match(i)
        if info:
            dinfo = info.groupdict()
            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            devices.append(dinfo)
print(devices)
'''
