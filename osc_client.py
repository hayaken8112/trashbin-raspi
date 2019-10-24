from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
import base64
import numpy as np
import cv2

img_file = "coke.jpeg"
b64_img = base64.encodestring(open(img_file, 'rb').read())
# print(b64_img)
# bin_img = base64.b64decode(b64_img)
# jpg = np.frombuffer(bin_img, dtype=np.uint8)

# img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
# cv2.imshow('dd', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

IP = '127.0.0.1'
PORT = 6700

# UDPのクライアントを作る
client = udp_client.UDPClient(IP, PORT)

# /colorに送信するメッセージを作って送信する
msg = OscMessageBuilder(address='/color')
msg.add_arg(0)
msg.add_arg(b64_img)
m = msg.build()

client.send(m)