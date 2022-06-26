from django.http import HttpResponse
from django.shortcuts import render
import cv2

# Create your views here.
def home(request):
    return render(request,'Enrollment.html')

def submitData(request):
    if request.method == 'POST':
        name = request.POST['name']
        sid = request.POST['sid']
        emailId = request.POST['email']
        img = request.POST['image']
        print(img)
        cv2.imshow("hello",img)
    return HttpResponse("<h1>Data</h1>")