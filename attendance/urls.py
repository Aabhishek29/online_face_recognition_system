from . import views
from django.urls import path

urlpatterns = [
    path('', views.enrollmentForm, name='enrollmentForm'),
    # path('submitData', views.submitData, name='submitData'),
    path('home',views.home,name='home'),
    # path('validateOTP',views.validateOTP,name="validateOTP"),
    path('openWebCam',views.openWebCam,name='openWebCam'),
    path('isImageVarified',views.isImageVarified,name='isImageVarified')
]
