from django.http import HttpResponse
from django.shortcuts import render
import cv2
from .models import EnrollStudent

# Create your views here.
def home(request):
    return render(request,'Enrollment.html')

def submitData(request):
    student = EnrollStudent()
    if request.method == 'POST':
        student.name = request.POST['name']
        student.sid = request.POST['sid']
        student.emailId = request.POST['email']
        print(request.POST['imgup'])
        try:
            student.img = request.POST['imgup']
        except Exception as e:
            print(e)
        print(student.img)
        student.save()
        # cv2.imshow("hello",img)
    return HttpResponse("<h1>Data</h1>")