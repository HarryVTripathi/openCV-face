import cv2
import os
import numpy as np
import MySQLdb
import ssl
import urllib.request
import webbrowser


subjects = ["", "Shailene woodley", "Elvis Presley" ,"Harsh Tripathi","Kristen Stewart","Arth Dubey","Jon Snow"]

db = MySQLdb.connect(host="localhost", user="root", passwd="you_think_iam_moron", db="harsh")   
cur = db.cursor()

for i in range(1,len(subjects)):
    cur.execute('insert image values (%s,%s,%s,%s,%s)',(i,subjects[i],'not_filled',0,0))
    db.commit()    
    
db.close()
