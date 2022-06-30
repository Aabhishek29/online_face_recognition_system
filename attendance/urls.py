from . import views
from django.urls import path

urlpatterns = [
    path('', views.enrollmentForm, name='enrollmentForm'),
    path('submitData', views.submitData, name='submitData'),
    path('home',views.home,name='home'),
]
