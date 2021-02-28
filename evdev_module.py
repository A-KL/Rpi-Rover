import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

def getByName(name):
    for device in devices:
        if name in device.name:
            return device