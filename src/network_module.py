import socket

CAMERA_H264_RAW_STREAM = "/tmp/camera_h264_stream.socket"

def get_interface():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 0))
    ipaddr = s.getsockname()[0]
    host = socket.gethostname()
    return ipaddr, host

if __name__ == "__main__":
    ip, host = get_interface()
    print ("IP:", ip, " Host:", host)