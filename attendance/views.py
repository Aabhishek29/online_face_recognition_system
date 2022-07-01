from asyncio.windows_events import NULL
import math
import random
import face_recognition
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
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

# Create your views here.
@gzip.gzip_page
def home(request):
    list_data = []
    val = EnrollStudent.objects.all()
    print(val)
    for i in val:
        list_data.append(i)
        print(i)
    return render(request, 'Enrollment.html',{'messages':list_data})


def openWebCam(request):
    try:
        data = request.GET['file_name']
    except Exception as e:
        print(e)
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(request,cam,data), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
    return render(request,'Enrollment.html')

def isImageVarified(request):
    pass


def enrollmentForm(request):
    form = EnrollmentForm()
    return render(request, 'Signup.html', {'form': form})


def submitData(request):
    global student_object
    global copy_instance
    if request.method == 'POST':
        print('fetching form data')
        # student = EnrollmentForm(request.POST, request.FILES)
        student_object.name = request.POST['name']
        student_object.emailId = request.POST['email']
        student_object.sid = request.POST['sid']
        student_object.img = request.FILES['imgup']

        copy_instance = student_object
        print(student_object.img)
        if validate_data(student_object) and send_otp(student_object.emailId):
            return render(request,'checkOtp.html')
        return HttpResponseRedirect('/')
    
    
def validateOTP(request):
    global student_object
    if request.method == 'GET':
        print("OTP verifing")
        firstVal = request.GET['input1']
        secondVal = request.GET['input2']
        thirdVal = request.GET['input3']
        fourthVal = request.GET['input4']

        val = firstVal+secondVal+thirdVal+fourthVal

        print(f'OTP genrated is: {otp_val} and OTP user entered is: {val}')
        print(f'OTP genrated is: {type(otp_val)} and OTP user entered is: {type(val)}')
        if(str(val)==str(otp_val)):
            print("OTP varified")
            if copy_instance!=None:
                copy_instance.save()
            else:
                print("Something went erong")
                return HttpResponse("Wrong")
            # if not detect_face(student_object.img):
            #     messages.add_message(request,1,"Face not recognised")
            #     student_object.delete()
            #     print("Face not found")
            #     return render(request,'Signup.html')
            student_object.clean()
            print("OTP varified sucessfully with image")
            return render(request,'SignUp.html')
        else:
            return HttpResponseRedirect('/')

    return HttpResponse("<h1>OTP Not Matched</h1>")


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self,request,imageName):
        jpeg = self.frame
        jpeg = cv2.cvtColor(jpeg,cv2.COLOR_BGR2RGB)
        aceloc = face_recognition.face_locations(jpeg)
        print(aceloc)
        try:
            if len(aceloc)==1:
                aceloc = aceloc[0]
                faceencode = face_recognition.face_encodings(jpeg)
                faceencode = faceencode[0]
                cv2.rectangle(jpeg, (aceloc[3], aceloc[0]), (aceloc[1], aceloc[2]), (255, 0, 255), 2)
                auth = EnrollStudent.objects.get(name=imageName)
                imgvar = face_recognition.load_image_file(f"media/{auth.img}")
                imgvar = cv2.cvtColor(imgvar,cv2.COLOR_BGR2RGB)

                faceloc = face_recognition.face_locations(imgvar)
                if len(faceloc) == 1:
                    faceencode2 = face_recognition.face_encodings(imgvar)[0]
                    flag = face_recognition.compare_faces(faceencode2,faceencode)
                    if flag==True:
                        return isImageVarified(request)
                    else:
                        return HttpResponse("Not")
        except Exception as e:
            self.video.release()
            print(e)

        _, jpeg = cv2.imencode('.jpg', jpeg)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(request,camera,data):
    while True:
        frame = camera.get_frame(request,data)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def validate_data(param)->bool:
    if len(param.name) < 2:
        return False
    temp = param.sid

    if len(temp) < 7 or not re.match(validstudentId,temp):
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