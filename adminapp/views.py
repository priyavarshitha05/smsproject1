
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import pytz
from . import models


def projecthomepage(request):
    return render(request, 'adminapp/projecthomepage.html')

def pagedividecall(request):
    return render(request, 'adminapp/pagediv.html')


def printpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'User input: {user_input}')
    a1 = {'user_input':user_input}
    return render(request, 'adminapp/pagediv.html',a1)


def excpetionpagecall(request):
    return render(request, 'adminapp/ExceptionExample.html')


def exceptionapagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10/num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/ExceptionExample.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/ExceptionExample.html')


import random
import string

def randompagecall(request):
    return render(request, 'adminapp/RandomExample.html')


def randomlogic(request):
    if request.method == "POST":
        number1 = int(request.POST['number1'])
        ran = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    a1 = {'ran':ran}
    return render(request, 'adminapp/RandomExample.html', a1)


def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

    return render(request, 'adminapp/calculator.html', {'result': result})

from .forms import Task_Form, StudentForm
from .models import Task, StudentList


def add_task(request):
    if request.method == "POST":
        form = Task_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = Task_Form()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html', {'form': form, 'tasks': tasks})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')




def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Validate inputs
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'adminapp/register.html')  # Render without redirect to avoid message accumulation

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email address.')
            return render(request, 'adminapp/register.html')  # Render without redirect to avoid message accumulation

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'adminapp/register.html')  # Render without redirect to avoid message accumulation

        # Create new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password  # Django handles password hashing
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('user_login')  # Redirect to the login page after successful registration

    return render(request, 'adminapp/register.html')  # Render the registration page initially


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check username length and redirect accordingly
            if len(username) == 10:
                messages.success(request, 'Student Login Successful!')
                return redirect('studentapp:student_homepage')
            elif len(username) == 4:
                messages.success(request, 'Faculty Login Successful!')
                return redirect('facultyapp:faculty_homepage')
            else:
                messages.error(request, 'Username length does not match any role-specific redirects.')
                return redirect('user_login')

        else:
            # If authentication fails, show an error message
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'adminapp/login.html', {'error_message': error_message})

    return render(request, 'adminapp/login.html')  # Render login page on GET request


def log_out(request):
    # Use Django's built-in logout function
    logout(request)
    # Redirect to a specific page after logging out (e.g., login page or homepage)
    return redirect(reverse('projecthomepage'))


def calculate_future_date(request):
    future_date = None
    if request.method == "POST":
        days_input = int(request.POST.get('days_input'))
        # Add the number of days to the current date
        current_time = timezone.now()
        future_date = current_time + timedelta(days=days_input)

    return render(request, 'adminapp/calculate_future_date.html', {
        'future_date': future_date
    })


def get_time_details(request):
    timezones = pytz.all_timezones
    timezone_time = None
    error_message = None
    timezone_name = None

    if request.method == 'POST':
        timezone_name = request.POST.get('timezone')
        try:
            # Get the current time in UTC
            utc_now = datetime.utcnow()

            # Convert UTC time to the selected timezone
            selected_timezone = pytz.timezone(timezone_name)
            timezone_time = utc_now.replace(tzinfo=pytz.utc).astimezone(selected_timezone)

            # Format the timezone_time for better readability (optional)
            timezone_time = timezone_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

        except pytz.UnknownTimeZoneError:
            error_message = "Invalid timezone selected. Please select a valid timezone."
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"

    return render(request, 'adminapp/time_details.html', {
        'timezones': timezones,
        'timezone_time': timezone_time,
        'timezone_name': timezone_name,
        'error_message': error_message,
    })


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projecthomepage')
    else:
        form = StudentForm()
    return render(request, 'adminapp/AddStudent.html', {'form': form})


def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student list.html', {'students': students})