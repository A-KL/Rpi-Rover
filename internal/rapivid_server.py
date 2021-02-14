import subprocess as sbp
import websockets
import asyncio
import time
import threading
import json
import array, fcntl, struct, select, os

NALseparator    = bytearray(b'\x00\x00\x00\x01'); #NAL break
current_frame   = bytearray(4096)

def stream(w, h, fps):
    cmd = f"raspivid -t 0 -o - -w {w} -h {h} -fps {fps} -pf baseline"
    data = bytearray(4096)

    with sbp.Popen(['raspivid', '-t', '0', '-o', '-', '-w', str(w), '-h', str(w), '-fps', str(fps), '-pf', 'baseline'], stdout=sbp.PIPE) as p:
        fd = p.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        streams = [ p.stdout ]
        temp0 = []
        readable, writable, exceptional = select.select(streams, temp0, temp0, 5)
        if len(readable) == 0:
            raise Exception("Timeout of 5 seconds reached!")
        
        while p.poll() is None:  # Check the the child process is still running
            received = p.stdout.readinto(data)
            if received == None or received <= 0:
                raise Exception("No data received!")
            yield received, data

def broadcast_thread():
    global current_frame
    for received, frame in stream(640, 480, 12):
        current_frame = frame

async def on_connected(client, uri):
    print("### connected ###")
    
    init = { "action":"init","width":640,"height":480 }
    await client.send(json.dumps(init))

    async for message in client:
        if(message == "REQUESTSTREAM "):
            while True:
                await client.send(NALseparator)
                await client.send(current_frame)

if __name__ == "__main__":
    server = websockets.serve(on_connected, "0.0.0.0", 8086)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)

    t = threading.Thread(target=broadcast_thread)
    t.start()

    loop.run_forever()