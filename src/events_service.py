import asyncio
import evdev
import mqtt_module as mqtt
import steering_module as steering
import evdev_module as input
import config_module as config

# Left
# ABS_X ABS_Y
# ABS_Z

# Right
# ABS_RX ABS_RY
# ABS_RZ

async def read_events(input):
    last = {
        "ABS_X": 128,
        "ABS_Y": 128,
        "ABS_Z": 0,
        "ABS_RX": 128,
        "ABS_RY": 128,
        "ABS_RZ": 0,
    }
    async for event in input.async_read_loop():
        # Buttons 
        # if event.type == evdev.ecodes.EV_KEY:
        #     print(event)

        # Analog
        if event.type == evdev.ecodes.EV_ABS:
            absevent = evdev.categorize(event)
            code = evdev.ecodes.bytype[absevent.event.type][absevent.event.code]
            if last[code] != absevent.event.value:
                last[code] = absevent.event.value
                motors_x = last["ABS_X"]
                motors_y = last["ABS_RZ"] - last["ABS_Z"]
                steering.updateMotors(client,(motors_x - 128) / 128, (motors_y - 128) / 128)
                print (code, absevent.event.value)

if __name__ == '__main__':
    client = mqtt.Create()
    gamepad = input.getByName('Sony')

    print(gamepad)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_events(gamepad))