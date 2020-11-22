import os
import json
import socket
import threading
import json
import picamera
import network_module as network
from quart import Quart, websocket, render_template, send_file

locations       = ['/home/pi/projects/Rover/assets/www', '/home/pi/projects/Rover/assets/www/vendor/dist']
app             = Quart(__name__)
camera_socket   = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

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
        buffer = camera_socket.recv(4096 * 5)

        # received = udp_socket.recv_into(buffer)
        await websocket.send(buffer)

if __name__ == '__main__':
    camera_socket.connect(network.CAMERA_H264_RAW_STREAM)
    print("Camera stream connected")
    app.run(host='0.0.0.0', debug=False)