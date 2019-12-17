import ssl
import urllib.request
import cv2
import webbrowser
import numpy as np

while True:
    context = ssl._create_unverified_context()
    res = urllib.request.urlopen("http://100.118.34.16:8080/shot.jpg",context = context)
    imgNp = np.array(bytearray(res.read()) , dtype = np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imdecode(imgNp,-1)
    cv2.imshow('im',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
