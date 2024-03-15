











from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from django.utils import timezone

from accounts.models import Attendance, Person
# import face_recognition
from .models import FaceEncoding,Visits,SystemUser
# from PIL import Image
import threading
import time

from django.http import HttpResponse

from django.http import StreamingHttpResponse
import numpy as np
import time
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .face_recognition_utils import predict, show_prediction_labels_on_image,train
import cv2
from django.http import JsonResponse
import os
from django.conf import settings

model_path = os.path.join(settings.MEDIA_ROOT, 'training_directory', 'trained_knn_model.clf')

train_dir = os.path.join(settings.MEDIA_ROOT, 'training_directory')



def index(request):
    # Retrieve initial visits data from the database or any other source
    return render(request, "index.html")

def live(request):
    # Retrieve initial visits data from the database or any other source
    return render(request, "live.html")

def latest_attendance(request):
    today = timezone.now().date()
    latest_attendance = Attendance.objects.filter(date=today).order_by('-entry_time')[:10]  # Fetch latest 10 attendances for today
    attendance_data = [{'user_name': attendance.person.system_user_name, 'time': attendance.entry_time} for attendance in latest_attendance]
    return JsonResponse({'latest_attendance': attendance_data})



# def realtime_visits(request):
#     initial_visits = Visits.objects.all()  # Fetch all visits from the database
#     context = {
#         'initial_visits': initial_visits,
#     }
#     return render(request, "realtime_visits.html", context)   
@require_GET
@login_required
def video_feed(request):
    def generate_frames():
        process_this_frame = 29
        cap = cv2.VideoCapture(0)  # or use any other video source

        # Variables to keep track of predictions within a 15-second window
        predictions_window = []
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if ret:
                # Resize the frame to improve streaming speed
                resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                process_this_frame += 1
                if process_this_frame % 30 == 0:
                    # Perform face recognition on the frame
                    predictions = predict(resized_frame, model_path=model_path)
                    if predictions:
                        name, _ = predictions[0]  # Access the name attribute from the first tuple
                        if name:
                            # Add the recognized name to the predictions_window
                            predictions_window.append(name)

                            # Check if 15 seconds have passed
                            elapsed_time = time.time() - start_time
                            if elapsed_time >= 15:
                                # Check if the recognized name occurred more than 4 times
                                if predictions_window.count(name) > 1:
                                    # Query the SystemUser associated with the predicted name
                                    system_user = Person.objects.filter(system_user_name=name).first()

                                    # Check if the system_user exists and its entry field is False
                                    if system_user and not system_user.entry:
                                        # Save the attendance record
                                        new_attendance = Attendance(person=system_user)
                                        new_attendance.save()

                                        # Update the entry field of the corresponding SystemUser to True
                                        system_user.entry = True
                                        system_user.save()

                                    # Reset the window and timer
                                    predictions_window = []
                                    start_time = time.time()

                print(predictions)
                frame_with_predictions = show_prediction_labels_on_image(resized_frame, predictions)

                # Convert the frame to JPEG format
                _, jpeg_frame = cv2.imencode('.jpg', frame_with_predictions)
                frame_bytes = jpeg_frame.tobytes()

                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
