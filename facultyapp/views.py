from django.core.mail import send_mail
from django.shortcuts import render

from facultyapp.forms import MarksForm


class Marksform:
    pass

    def PostMarks(request):
        if request.method == "POST":
            form = Marksform(request.POST)
            if form.is_valid():
                marks_instance = form.save(commit=False)
                marks_instance.save()

                # Retrieve the User email based on the student in the form
                student = marks_instance.student
                student_user = student.user
                user_email = student_user.email

                subject = 'Marks Entered'
                message = f'Hello, {student_user.first_name}  marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
                from_email = 'boyapati.thanmaisree@gmail.com'
                recipient_list = [user_email]
                send_mail(subject, message, from_email, recipient_list)

                return render(request, 'facultyApp/marks_success.html')
        else:
            form = Marksform()
        return render(request, 'facultyApp/PostMarks.html', {'form': form})

def faculty_homepage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')
