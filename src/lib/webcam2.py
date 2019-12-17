import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break
    elif key == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('test-data/test_temp.jpg',frame)


cv2.destroyWindow("preview")
vc.release()
