# import the necessary packages
import time
import websocket
import cv2

def on_open(ws):
    print("Open")

def on_message(ws, message):
    # print(message)
    imagedisp = cv2.imdecode(message, 1)
    cv2.imshow("Frame", imagedisp)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    cv2.destroyAllWindows()