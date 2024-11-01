from django.shortcuts import render

# Create your views here.


def student_homepage(request):
    return render(request, 'studentapp/StudentHomePage.html')
