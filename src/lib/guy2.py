import tkinter as tk
import cv2
import os
import numpy as np
import MySQLdb
import ssl
import urllib.request
import webbrowser

class Main:
    def createGui(self):
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
            self.leftFrame = tk.Frame(root, width=400, bg="black", height=650, borderwidth=3, relief=tk.FLAT)
            self.rightFrame = tk.Frame(root, width=400, bg="black", height=650)

            mainLabel = tk.Label(self.leftFrame, text="Recognizing Faces..", fg="white", bg="black", font=('Comic Sans MS', 18, 'bold'))
            mainLabel.grid(row=0, columnspan=3)

            path = "test-data"

            attendanceLabel = tk.Label(self.rightFrame, text="Attendance Status", bg="black", fg="white", font=('Helvetica', 18, 'bold'))

            attendanceLabel.grid(row=0, columnspan=2, pady=(100, 20), padx=(100,100))
            n=1
            for i in range(1001,1060):
                label = tk.Label(self.rightFrame, bg="black", text="15BCE"+str(i)+"      :", fg="white")
                label.grid(row=n, column=0, padx=(20,20), sticky=tk.E)
                n = n+1


            button1 = tk.Button(self.leftFrame, text="Display Result", bg="white", fg="black", font=('Helvetica', 14),command = self.train)
            button2 = tk.Button(self.leftFrame, text="Show attendance", bg="white", fg="black", font=('Helvetica', 14), command =self.detect_face)
            button3 = tk.Button(self.leftFrame, text="Take attendance", bg="white", fg="black", font=('Helvetica', 14), command=self.prepare_training_data)

            button1.grid(row=2, column=1, pady=(20, 20))
            button2.grid(row=3, column=1, pady=(20, 20))
            button3.grid(row=4, column=1, pady=(20, 20))


            self.leftFrame.pack(side=tk.LEFT)
            self.rightFrame.pack()

            root.mainloop()

    def detect_face(img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
            
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
                
                #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                #cv2.waitKey(100)
                
                face, rect = detect_face(image)
                
                if face is not None:
                    faces.append(face)
                    labels.append(label)
                
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        
        return faces, labels

    def predict(test_img):

        img = test_img.copy()
        face, rect = detect_face(img)
        label, confidence = face_recognizer.predict(face)
        label_text = subjects[label]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5)
        
        return img,label_text

    def train():
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

        


if __name__ == "__main__":
    print("start")
    obj = Main()
    obj.createGui()
    
