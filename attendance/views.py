from sys import stdout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import cv2
from .models import EnrollStudent
from .form import EnrollmentForm
from django.contrib import messages

# Create your views here.
def home(request):
    form = EnrollmentForm()
    return render(request,'Signup.html',{'form':form})

def submitData(request):
    if request.method == 'POST':
        print('fetching form data')
        student = EnrollmentForm(request.POST,  request.FILES)
        print(student)
        # handle_uploaded_file(request.FILES['img'])  
        student.save()
        # if student.is_valid():
        #     student.save()
        #     print("Successfully Done...")
        #     messages.info(request,"Successfully Done...")
        # else:
        #     print("Something went wrong...")
        #     messages.info(request,"Something went wrong...")
        #     return HttpResponseRedirect('/')
    return HttpResponse("<h1>Data</h1>")

# def handle_uploaded_file(f):  
#     with open('online_face_recognition_system/static/images/'+f.name, 'wb+') as destination:  
#         for chunk in f.chunks():  
#             destination.write(chunk)


