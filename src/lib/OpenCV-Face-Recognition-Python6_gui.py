import cv2
import os
import numpy as np
import MySQLdb
import ssl
import urllib.request
import webbrowser
import tkinter as tk

from pygame import mixer 

mixer.init()
mixer.music.load('hello2.mp3')
mixer.music.play()


subjects = ["", "Shailene woodley", "Elvis Presley" ,"Harsh Tripathi","Kristen Stewart","Joey Tribbiany","Jon Snow"]

db = MySQLdb.connect(host="localhost", user="root", passwd="well, maybe", db="harsh")   
cur = db.cursor()


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): 
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(1)
    if key == 27: 
        break
    elif key == ord('s'): 
        cv2.imwrite('test-data/test_temp.jpg',frame)


cv2.destroyWindow("preview")
vc.release()



def detect_face(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.03, minNeighbors=5 );
     
    if (len(faces) == 0):
        return None, None
    
    (x, y, w, h) = faces[0] 
    return gray[y:y+w, x:x+h], faces[0]


def prepare_training_data(data_folder_path):
    
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
            
        label = int(dir_name.replace("s", ""))
        
        subject_dir_path = data_folder_path + "/" + dir_name
        
        subject_images_names = os.listdir(subject_dir_path)
        
        for image_name in subject_images_names:
            
            if image_name.startswith("."):
                continue;
            
            image_path = subject_dir_path + "/" + image_name

            image = cv2.imread(image_path)
            
            cv2.imshow("Training on image...", cv2.resize(image, (400,500)))
            cv2.waitKey(100)
            
            face, rect = detect_face(image)
            
            if face is not None:
                faces.append(face)
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels


print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")

print("Total faces: ", len(faces))
print("Total labels: ", len(labels))




face_recognizer = cv2.face.LBPHFaceRecognizer_create()


face_recognizer.train(faces, np.array(labels))


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)



def predict(test_img):

    img = test_img.copy()
    face, rect = detect_face(img)
    label, confidence = face_recognizer.predict(face)
    
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    
    return img,label_text

print("Predicting images...")







test_img = cv2.imread("test-data/test_temp.jpg")
predicted_img,name = predict(test_img)

print(name)



print("Prediction complete")

def display(predicted_img):
    cv2.imshow("cam", cv2.resize(predicted_img, (400, 500)))
    

cur.execute('update image set present=present+1 where name=%s',[name])
db.commit()











root = tk.Tk()
root.wm_title("Attendance Updater")

root.configure(bg="black")

w = 800 # width for the Tk root
h = 650 # height for the Tk root

ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

                # calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
leftFrame = tk.Frame(root, width=400, bg="black", height=650, borderwidth=3, relief=tk.FLAT)
rightFrame = tk.Frame(root, width=400, bg="black", height=650)

mainLabel = tk.Label(leftFrame, text="Recognizing Faces..", fg="white", bg="black", font=('Comic Sans MS', 18, 'bold'))
mainLabel.grid(row=0, columnspan=3)

path = "test-data"

attendanceLabel = tk.Label(rightFrame, text="VIT UNIVEERSITY ATTENDENCE SYSTEM", bg="black", fg="white", font=('Helvetica', 18, 'bold'))

attendanceLabel.grid(row=0, columnspan=2, pady=(100, 20), padx=(100,100))
cur.execute("SELECT * FROM image")
n = 1
for row in cur.fetchall():
    label1 = tk.Label(rightFrame, bg="black", text=row[1]+"      :", fg="white")
    label2 = tk.Label(rightFrame, bg="black", text=str(row[3])+" ", fg="white")
    label1.grid(row=n, column=0, padx=(20,20), sticky=tk.E)
    label1.grid(row=n, column=0, padx=(20,20), sticky=tk.E)
    n = n+1


button1 = tk.Button(leftFrame, text="Display Result", bg="white", fg="black", font=('Helvetica', 14),command =  lambda: display(predicted_img))
button3 = tk.Button(leftFrame, text="Take attendance", bg="white", fg="black", font=('Helvetica', 14), command=prepare_training_data)

button1.grid(row=2, column=1, pady=(20, 20))
#button2.grid(row=3, column=1, pady=(20, 20))
button3.grid(row=4, column=1, pady=(20, 20))


leftFrame.pack(side=tk.LEFT)
rightFrame.pack()



db.close()


cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()





