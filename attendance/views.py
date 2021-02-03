from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.urls import reverse
import os
import datetime
import numpy as np
import cv2
from PIL import Image
import pandas as pd
import threading
from functools import partial
import json 
# Create your views here.

def index(request):
    return render(request,'attendance/attendance.html')
def face(request):
    return render(request,'attendance/dataset.html')
def showAttendance(request):
    Dir = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(Dir + '/Attendance/Attendance.csv')
    json_records = df.reset_index().to_json(orient ='records') 
    data = [] 
    data = json.loads(json_records)
    df1 = df.loc[df['id'] == int(request.user.id)].iloc[0]
    # df1 = df1.drop(df1.iloc[:, 0:2], inplace = True, axis = 1)
    df1 = df1[0:].values
    return render(request,'attendance/show_attendance.html',{'data':data,'colls':data[0],'dataframe':df1})
running = False
message = ''

def showMsg(request):
    global message
    return HttpResponse(message)

def mark(request):
    global running
    running = False
    return HttpResponse('')

def stream(request):
    global running
    running=True
    return StreamingHttpResponse(Attendence(request),content_type='multipart/x-mixed-replace; boundary=frame')
def Attendence(request):
    global message
    Dir = os.path.dirname(os.path.realpath(__file__))
    dataset_path = path = os.path.join(Dir, 'dataset') 
    if not (os.path.isdir(dataset_path)):
        os.mkdir(dataset_path)
    try:
        user_id = int(request.user.id)
        date = datetime.date.today()
        eye = cv2.CascadeClassifier(Dir + '/haarcascade_eye.xml')
        recog = cv2.face.LBPHFaceRecognizer_create()
        recog.read(Dir + '/trainer/trainer.yml')
        face = cv2.CascadeClassifier(Dir + '/haarcascade_frontalface_default.xml')

        font = cv2.FONT_HERSHEY_DUPLEX

        rec = 0
        id = 0
        face_numbers = 5
        camera = cv2.VideoCapture(0)
        camera.set(3, 1280)
        camera.set(4, 720)

        minWidth = 0.01*camera.get(3)
        minHeight = 0.01*camera.get(4)
        blink = 0
        is_eye = False
        while running:
            rtrn, image=camera.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face.detectMultiScale( 
                gray,
                scaleFactor = 1.3,
                minNeighbors = face_numbers,
                minSize = (int(minWidth), int(minHeight)),
            )
            eyes = eye.detectMultiScale(image,scaleFactor = 1.2, minNeighbors = 5) 
            for (x, y, w, h) in eyes: 
                cv2.rectangle(image, (x, y),  
                            (x + w, y + h), (255, 0, 0), 1)
            if len(eyes) >= 2:
                is_eye = True
                cv2.putText(image, "eye detected", (50,50), font, 1, (0,255,0), 1)
            if(len(faces)==0):
                blink = 0
            if len(eyes) < 2:
                blink+=1
            cv2.putText(image, "Blink(16+) : {}".format(blink), (1020,50), font, 1, (0,0,255), 2)
            for(x,y,w,h) in faces:
                id, match = recog.predict(gray[y:y+h,x:x+w])
                if (id == user_id) and (match < 45):
                    rec = 1
                    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                    try:
                        df = pd.read_csv(Dir + '/list/students.csv')
                        name = df.loc[df['id'] == id, 'name'].iloc[0]
                    except:
                        name = "Unknown"
                    match = "  {0}%".format(round(100 - match))
                else:
                    rec = 0
                    cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                    name = "unknown"
                    match = "  {0}%".format(round(100 - match))
                cv2.putText(image, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(image, str(match), (x+5,y+h-5), font, 1, (255,255,0), 1)
            ret, frame = cv2.imencode('.jpg',image)
            yield (b'--frame\r\n'
                    b'Content-Type:image/jpeg\r\n\r\n'+frame.tobytes()+b'\r\n\r\n')
            k = cv2.waitKey(1)
            if k == 27:
                break
        if rec==1 and blink >15:
            df = pd.read_csv(Dir + '/Attendance/Attendance.csv')
            coll = ['0']*len(df['id'])
            if str(date) in df.columns:
                if (int(df.loc[df['id'] == id, str(date)].iloc[0]))==0:
                    df.loc[df['id'] == id, str(date)]=1
                    df.to_csv(Dir + '/Attendance/Attendance.csv', index=False)
                    message = "Attendance entered successfully."
                    print("Attendance entered successfully.")
                else:
                    message = "Attendance already exist"
                    print("Attendance already exist.")
            else:
                df[str(date)] = coll
                df.loc[df['id'] == id, str(date)]=1
                df.to_csv(Dir + '/Attendance/Attendance.csv', index=False)
                message = "Attendance entered successfully."
                print("Attendance entered successfully.")
        else:
            message = "Attendance not entered"
            print("Attendance not entered.")
        camera.release()
        cv2.destroyAllWindows()
    except Exception as e:
        message = "Some error occured. Try again!"
        print("Some error occured. Try again!",e)
    return HttpResponse(message)

def dataset(request):
    global message
    Dir = os.path.dirname(os.path.realpath(__file__))
    dataset_path = path = os.path.join(Dir, 'dataset') 
    if not (os.path.isdir(dataset_path)):
        os.mkdir(dataset_path)
    try:
        name = str(request.user.first_name) + ' ' + str(request.user.last_name)
        face_id = str(request.user.id)
        snap_amount = 200
        camera = cv2.VideoCapture(0)
        camera.set(3, 1280)
        camera.set(4, 720)

        face = cv2.CascadeClassifier(Dir + '/haarcascade_frontalface_default.xml')
        if len(face_id)<=0 or len(name)<=0 or snap_amount <=0:
            message = "All Fields Required"
        else:
            count = 0
            while True:
                rtrn, image=camera.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face.detectMultiScale(gray, 1.3, 5)

                for(x,y,w,h) in faces:
                    cv2.rectangle(image, (x,y),(x+w,y+h),(255,0,0),2)
                    count+=1

                    cv2.imwrite(Dir + "/dataset/"+str(name)+"_" + str(face_id) + '_' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('image', image)
                wait = cv2.waitKey(10) & 0xff
                if wait == 27:
                    break
                elif count >=snap_amount:
                    break
            camera.release()
            cv2.destroyAllWindows()
            try:
                exist = False
                df = pd.read_csv(Dir + '/list/students.csv')
                for i in range(len(df['id'])):
                    if df['id'].iloc[i] == int(face_id):
                        exist = True
                if not exist:
                    df.loc[len(df.index)] = [int(face_id),name]
                    df.to_csv(Dir + '/list/students.csv', index=False)
                df1 = pd.read_csv(Dir + '/Attendance/Attendance.csv')
                for i in range(len(df1['id'])):
                    if df1['id'].iloc[i] == int(face_id):
                        exist = True
                if not exist:
                    arr = [int(face_id),name]
                    arr = np.concatenate((arr,[0]*(len(df1.columns)-2)))
                    df1.loc[len(df1.index)] = arr
                    df1.to_csv(Dir + '/Attendance/Attendance.csv', index=False)
            except Exception as e:
                print(e)
            message = "Face included successfully. Please train the system."
    except Exception as e:
        message = "Some error occured. Try again!"
        print(e)
    return HttpResponse(message)

def getImage_Labels(dataset,face):
    imagesPath=[os.path.join(dataset,f) for f in os.listdir(dataset)]
    faceSamples = []
    ids = []
    for imagePath in imagesPath:
        PIL_img=Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        id=int(os.path.split(imagePath)[-1].split("_")[1])
        faces = face.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
def train(request):
    global message
    Dir = os.path.dirname(os.path.realpath(__file__))
    dataset_path = path = os.path.join(Dir, 'dataset') 
    if not (os.path.isdir(dataset_path)):
        os.mkdir(dataset_path)
    message = "Training Faces."
    dataset = Dir + '/dataset'
    recog = cv2.face.LBPHFaceRecognizer_create()
    face = cv2.CascadeClassifier(Dir + '/haarcascade_frontalface_default.xml')

    faces,ids=getImage_Labels(dataset,face)
    recog.train(faces, np.array(ids))

    recog.write(Dir + '/trainer/trainer.yml')

    message = str(len(np.unique(ids))) + " face trained."
    return HttpResponse(message)