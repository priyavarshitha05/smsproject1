from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'facultyapp'

urlpatterns = [
    path('faculty_homepage/', views.faculty_homepage, name='faculty_homepage')
]
