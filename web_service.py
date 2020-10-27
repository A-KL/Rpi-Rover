import sys
import socketserver
from http.server import SimpleHTTPRequestHandler

import base64

import io
import time
import picamera

class MJpegHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=myboundary')
        self.end_headers()

        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            time.sleep(2)
            #while True:
            stream.truncate()
            stream.seek(0)
            camera.resolution = (640, 480)
            camera.capture(stream, 'jpeg')
            output = "--myboundary\r\n"
            output += "Content-Type: image/jpeg\r\n"
            output += f"Content-length: {stream.getbuffer().nbytes}\r\n\r\n"
            output += base64.b64encode(stream.getvalue()).decode('utf_8')
            output += "\r\n"
            self.wfile.write(output.encode(encoding = 'utf_8'))

if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MJpegHandler) as httpd:
        print("Listening on port {}. Press Ctrl+C to stop.".format(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting Down!")
            httpd.server_close()    