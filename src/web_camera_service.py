import os
import json
import socket
import json
import io
from picamera import *
from threading import *
from quart import *

locations = ['/home/pi/projects/Rpi-Rover/assets/www', '/home/pi/projects/Rpi-Rover/assets/www/vendor/dist']
app       = Quart(__name__)

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\x00\x00\x00\x01'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

@app.route('/')
async def index():
    return await findFile(locations, 'index.html')

@app.route('/<file>')
async def action(file):
    if (file is None):
        return await index()
    else:
        return await findFile(locations, file)
    
async def findFile(locations, file):
    for location in locations:
        try:
            fullPath = os.path.join(location, file)
            return await send_file(fullPath)
        except:
            print(f"Failure!")
    return ""

@app.websocket('/')
async def connected():
    init = { "action":"init","width":640,"height":480 }

    await websocket.send(json.dumps(init))

    while websocket.endpoint == "connected":
        with output.condition:
            output.condition.wait()
            await websocket.send(output.frame)

if __name__ == '__main__':
    output = StreamingOutput()

    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 12
        camera.start_recording(output, format='h264', quality=20, profile='baseline')

        app.run(host='0.0.0.0', debug=False)