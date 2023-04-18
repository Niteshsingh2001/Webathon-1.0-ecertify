import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
import json


def index(request):
    if request.method == 'POST':
        admin = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=admin, password=password)
        if user is not None:
            login(request, user)
            cont = {"name": user, "status": True}
            print("done")
            return redirect("dashboard")
        else:
            cont = {"error": "Something went wrong!! "}
            print(user)
            return render(request, 'admin_signup.html', cont)

    return render(request, "admin_signup.html")


@login_required(login_url='/admin')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='/admin')
def logout_view(request):
    logout(request)
    return redirect('/admin')


def add_student(request):
    if request.method == 'POST':
        # Get data from POST request
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['mail']
        dob = request.POST['date']
        # Create student object
        student = Student(username=username, name=name, email=email, dob=dob)

        # Save student object to database
        student.save()

        # Redirect to success page
        return JsonResponse({"status": "success"})

    # Render the template for adding student data
    return render(request, 'dashboard.html')


def delete_student(request, id):
    data = get_object_or_404(Student, id=id)
    if request.method == 'GET':
        data.delete()
        return JsonResponse({"status": "success"})
    return render(request, 'dashboard.html')


def edit_student(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == 'POST':
        print("*********************")
        print(request.POST.get('edit_date'))
        student.username = request.POST.get('edit_username')
        student.name = request.POST.get('edit_name')
        student.email = request.POST.get('edit_mail')
        student.dob = request.POST.get('edit_date')
        student.save()
        data = {'success': True}
        return JsonResponse(data)

    if request.method == 'GET':
        data = {
            'id': student.id,
            'username': student.username,
            'name': student.name,
            'email': student.email,
            'dob': student.dob,
        }
        return JsonResponse(data)

    return render(request, 'dashboard.html')


def student_data(request):
    my_data = Student.objects.all()
    data = [{"id": obj.id, "username": obj.username, "name": obj.name, "mail": obj.email, "dob": obj.dob}
            for obj in my_data]
    return JsonResponse(data, safe=False)


def studentInterface(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        dob = request.POST.get('dob')

        students = Student.objects.get(username=username, dob=dob)
        data = {"name": students.name, "certifcate": students.certificate}

        return JsonResponse(data)

    return render(request, "studentInterface.html")


def generate(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == 'POST':
        data = {
            "msg": request.POST.get('gen_msg'),
            "purpose": request.POST.get('gen_purpose'),
            "date": datetime.date.today().isoformat()
        }
        if student.certificate:
            student.certificate.append(data)
        else:   
            student.certificate = [data]
        student.save()
        data = {'success': True}
        return JsonResponse(data)
    return render(request, "certificate.html")
