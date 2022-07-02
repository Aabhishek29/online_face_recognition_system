from ast import arg
from asyncio.windows_events import NULL
import email
import math
import random
from cv2 import setTrackbarPos
import django
import face_recognition
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render,redirect
import cv2
from django.views.decorators import gzip
from requests import request
from .models import EnrollStudent
from .form import EnrollmentForm
from django.contrib import messages
import threading
import re

validNameRegex = re.compile(r'^([a-z]+)*( [a-z]+)*$',re.IGNORECASE)

validstudentId = '^[0-9]+$'

student_object = EnrollStudent()
copy_instance = EnrollStudent()

copy_instance = None

otp_val = "0000"


VID_FLAG = 0

# Create your views here.

def home(request):
    list_data = ['---Select---']
    try:
        val = EnrollStudent.objects.all()
        print(val)
        for i in val:
            list_data.append(i)
            print(i)
    except Exception as e:
        print(e)
    if len(list_data) == 0:
        list_data = "No Data in Database"
    return render(request, 'Enrollment.html',{'messages':list_data})

@gzip.gzip_page
def openWebCam(request):
    global VID_FLAG
    if VID_FLAG == 0 or VID_FLAG == 1:
        print("-----------------------------0------------------------------------------")
        try:
            data = request.GET['person']
        except Exception as e:
            print(e)
        try:
            cam = VideoCamera()
            genval = gen(request,cam,data)
            print(f"%%%%%%%%%%%%%%%%%%%    {type(genval)}")
            if VID_FLAG == 1:
                print("working bhai")
                VID_FLAG = 0
                return redirect("home")
            return StreamingHttpResponse(genval, content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:
            print(e)
    elif VID_FLAG == 1:
        print("------------------------------------1---------------------------------------")
        return render(request,'Enrollment.html',{'value':True})
    return render(request,'Enrollment.html')

def isImageVarified(request):
    return HttpResponse("<h1>hello</h1>")


def enrollmentForm(request):
    name = ""
    emailId= ""
    sid = ""
    img = ""
    if request.method == 'POST':
        if 'signupbtn' in request.POST:
            print('fetching form data')
        # student = EnrollmentForm(request.POST, request.FILES)
            name = request.POST['name']
            emailId = request.POST['email']
            sid = request.POST['sid']
            if validate_data(name,sid) and send_otp(emailId):
                return render(request,'Signup.html',{'flag':0,'name':name,'sid':sid,'emailId':emailId})
        elif 'otpbtn' in request.POST:
            firstVal = request.POST['input1']
            secondVal = request.POST['input2']
            thirdVal = request.POST['input3']
            fourthVal = request.POST['input4']
            name = request.POST['name']
            emailId = request.POST['email']
            sid = request.POST['sid']
            img = request.FILES['imgup']

            val = firstVal+secondVal+thirdVal+fourthVal

            print(f'OTP genrated is: {otp_val} and OTP user entered is: {val}')
            print(f'OTP genrated is: {type(otp_val)} and OTP user entered is: {type(val)}')
            if(str(val)==str(otp_val)):
                print("OTP varified")
                print(f'{name} {sid} {emailId}')
                student_object = EnrollStudent()
                student_object.name = name
                student_object.sid = sid
                student_object.emailId = emailId
                student_object.img = img
                print(img)
                if student_object!=None:
                    print(student_object)
                    student_object.save()
                else:
                    print("Something went erong")
                    return HttpResponse("Wrong")
                student_object.clean()
                print("OTP varified sucessfully with image")
                return render(request,'SignUp.html',{'flag':1})
            else:
                print("otp not varified")
                return HttpResponseRedirect('/')
        return HttpResponse("<h1>OTP Not Matched</h1>")
    return render(request, 'Signup.html', {'flag':1})


class VideoCamera(object):
    def __init__(self):
        self.waiting_time = 0
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self,request,imageName):
        jpeg = self.frame
        try:
           
            aceloc = face_recognition.face_locations(jpeg)
            print(aceloc)
            if len(aceloc)==1:
                aceloc = aceloc[0]
                faceencode = face_recognition.face_encodings(jpeg)
      
                if len(faceencode) == 1:
                    faceencode = faceencode[0]
            
                cv2.rectangle(jpeg, (aceloc[3], aceloc[0]), (aceloc[1], aceloc[2]), (255, 0, 255), 2)
       
                auth = EnrollStudent.objects.get(name=imageName)
             
                try:
                    imgvar = face_recognition.load_image_file(f"media/{auth.img}")
                    print(f"media/{auth.img}")
                    # imgvar = cv2.cvtColor(imgvar,cv2.COLOR_BGR2RGB)
                    # imgVar = cv2.rotate(imgVar, cv2.ROTATE_90_COUNTERCLOCKWISE)
                except Exception as e:
                    print("there is some issue in line number 162 ",e)
   
                faceloc = face_recognition.face_locations(imgvar)
              
                if len(faceloc) == 1:
                    faceencode2 = face_recognition.face_encodings(imgvar)[0]
                    # try:
                    #     # print(faceencode2)
                    #     # print(faceencode)
                    #     flag = face_recognition.compare_faces(faceencode2,faceencode)
                    # except Exception as e:
                    #     print("Image compare Execption")
                    # if flag==True:
                    #     print("True image face detected")
                    #     return isImageVarified(request)
                    # else:
                    #     print("not detected")
                    #     return HttpResponse("Not")
        except Exception as e:
            self.video.release()
            print("there is some issue in line number 175 ",e)
        self.waiting_time += 1
        print(self.waiting_time)
        global VID_FLAG
        if self.waiting_time == 50:
            self.video.release()
            VID_FLAG = 1
            return HttpResponse("hello")
        _, jpeg = cv2.imencode('.jpg', jpeg)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(request,camera,data):
    while True:
        frame = camera.get_frame(request,data)
        if isinstance(frame,HttpResponse):
            print("hello bhai")
            setTrackbarPos(10)
            return redirect('Enrollment.html')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def validate_data(name,sid)->bool:
    if len(name) < 2:
        return False

    if len(sid) < 7 or not re.match(validstudentId,sid):
        return False
    return True

def detect_face(img):
    imgvar = face_recognition.load_image_file(f"media/images/{img}")
    imgvar = cv2.cvtColor(imgvar,cv2.COLOR_BGR2RGB)

    faceloc = face_recognition.face_locations(imgvar)
    if len(faceloc) == 1:
        return True
    return False

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(emailId):
    email = emailId
    print(email)
    global otp_val
    otp_val=generateOTP()
    print(otp_val)
    htmlgen = f'<p>Your OTP is <strong>{otp_val}</strong></p>'
    a = send_mail('OTP request',otp_val,'starkabhishek29@gmail.com',[email], fail_silently=False, html_message=htmlgen)
    if(a==0):
        print('not send')
        return False
    else:   
        print('sent succesfully')
    return True


def adminPanel(request):
    return HttpResponseRedirect('admin')