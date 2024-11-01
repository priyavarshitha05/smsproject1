from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('student_homepage/', views.student_homepage, name='student_homepage')
]