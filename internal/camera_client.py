import socket
from threading import Thread
from time import sleep
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 5005))

if __name__ == '__main__':
    while True:
        try:
            #Attempt to receive up to 1024 bytes of data
            data, addr = s.recvfrom(4048)
            print(f"Received from {addr}. Message: {len(data)}")

        except socket.error:
            #If no data is received, you get here, but it's not an error
            #Ignore and continue
            pass