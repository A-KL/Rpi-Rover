import os
import json
import socket
import threading
import json
import picamera
from quart import Quart, websocket, render_template, send_file

locations       = ['/home/pi/projects/Rover/assets/www', '/home/pi/projects/Rover/assets/www/vendor/dist']
current_frame   = bytearray(4096)
app             = Quart(__name__)

class WriteCallbackStream(object):
    def __init__(self, write_callback):
        self.write_callback = write_callback

    def write(self, buf):
        return self.write_callback(buf)

def on_new_raw_frame(buffer):
    global current_frame
    current_frame = buffer

@app.route('/')
async def index():
    return await findFile(locations, 'index.html')

@app.route('/<file>')
async def action(file):
    if (file is None):
        return await index()
    else:
        return await findFile(locations, file) or ""
    
async def findFile(locations, file):
    for location in locations:
        try:
            fullPath = os.path.join(location, file)
            return await send_file(fullPath)
        except:
            print(f"Failure!")
    return None

@app.websocket('/')
async def connected():
    init = { "action":"init","width":640,"height":480 }

    await websocket.send(json.dumps(init))

    while websocket.endpoint == "connected":
        global current_frame
        await websocket.send(current_frame)

if __name__ == '__main__':
    stream = WriteCallbackStream(on_new_raw_frame)

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 12
        camera.start_recording(stream, format='h264', quality=20, profile='baseline')

        app.run(host='0.0.0.0', debug=False)