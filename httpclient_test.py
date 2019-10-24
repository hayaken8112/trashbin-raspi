import requests
import cv2
import base64

b64_img = base64.encodestring(open('./coke.jpeg', 'rb').read())

response = requests.post('http://localhost:8080', data=b64_img)
print(response.status_code)    # HTTPのステータスコード取得
print(response.text)    # レスポンスのHTMLを文字列で取得