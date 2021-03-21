import sys
import socketserver
from http.server import SimpleHTTPRequestHandler
import io
import time
import picamera

PAGE="""\
<html>
<head>
<title>SkyWeather MJPEG streaming demo</title>
</head>
<body>
<h1>SkyWeather MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class MJpegHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()

        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=myboundary')
            self.end_headers()

            with picamera.PiCamera() as camera:
                stream = io.BytesIO()
                camera.resolution = (640, 480)
                camera.framerate = 5
                camera.start_preview()
                time.sleep(2)

                for foo in camera.capture_continuous(stream, 'jpeg'):
                    stream.seek(0)

                    if (self.wfile.closed):
                        return

                    self.wfile.write(b'--myboundary\r\n')

                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', stream.tell())
                    self.end_headers()

                    stream.seek(0)
                    self.wfile.write(stream.read())
                    self.wfile.write(b'\r\n')

                    stream.seek(0)
                    stream.truncate()

if __name__ == '__main__':
    with socketserver.TCPServer(("", 8086), MJpegHandler) as httpd:
        print("Listening on port {}. Press Ctrl+C to stop.".format(8086))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting Down!")
            httpd.server_close()    