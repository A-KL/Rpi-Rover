import socket

def get_interface():
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    ipaddr = s.getsockname()[0]
    host = socket.gethostname()
    return ipaddr, host

if __name__ == "__main__":
    ip, host = get_interface()
    print ("IP:", ip, " Host:", host)