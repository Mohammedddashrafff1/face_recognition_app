
import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import *
 
from django.http import HttpResponse, JsonResponse, Http404
from datetime import datetime

from django.shortcuts import render
from .models import Attendance, Person
from django.db.models import Q

def search_attendance(request):
    persons = Person.objects.all()  # Assuming you have this queryset in your view

    if request.method == 'GET':
        person_id = request.GET.get('person')
        date_from_str = request.GET.get('registration_date_from')
        date_to_str = request.GET.get('registration_date_to')

        # Convert date strings to datetime objects
        try:
            date_from = datetime.strptime(date_from_str, '%Y/%m/%d').date() if date_from_str else None
            date_to = datetime.strptime(date_to_str, '%Y/%m/%d').date() if date_to_str else None
        except ValueError:
            return render(request, 'error.html', {'error_message': 'Invalid date format'})

        # Build the query dynamically based on the input values
        attendance_results = Attendance.objects.all()

        if person_id:
            attendance_results = attendance_results.filter(person_id=person_id)

        if date_from:
            attendance_results = attendance_results.filter(date__gte=date_from)

        if date_to:
            attendance_results = attendance_results.filter(date__lte=date_to)

        return render(request, 'attendance_search.html', {'attendance_results': attendance_results, 'persons': persons, 'selected_person': int(person_id) if person_id else None})

    return render(request, 'attendance_search.html', {'persons': persons})

def home(request):
    # Retrieve initial visits data from the database or any other source
    if request.user.is_authenticated:
        return redirect('website:index')
    else:
        return redirect("login")


def login_view(request):
    if request.method=="POST":
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('website:index')
        else:
            error_message = 'Invalid username or password.'
            return render(request, "/login.html", {'error_message': error_message})
    return render (request,'login.html')   


def logout_view(request):
    logout(request)
    return redirect("accounts:login")



def add_face(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        document_file = request.FILES.get('document_file')

        if username and document_file:
            # Create a new Person instance
            person = Person(system_user_name=username)
            person.save()

            # Create a new Image instance linked to the person
            image = Image(person=person, document_file=document_file)
            image.save()

            

    return render(request, 'add_face.html')  



def add_image(request):
    persons = Person.objects.all()

    if request.method == 'POST':
        person_id = request.POST.get('person')
        document_file = request.FILES.get('document_file')

        if person_id and document_file:
            person = Person.objects.get(pk=person_id)

            # Create a new Image instance linked to the selected person
            image = Image(person=person, document_file=document_file)
            image.save()

          

    context = {'persons': persons}
    return render(request, 'add_image_to_person.html', context)





      


