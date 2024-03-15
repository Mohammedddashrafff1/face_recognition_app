from django.urls import path
from .views import video_feed,index,live,latest_attendance



app_name = 'website'


urlpatterns = [
    path('', index, name='index'),
    path('video_feed', video_feed, name='video_feed'),
    path('live/',live, name='live'),
    path('latest_attendance/',latest_attendance, name='latest_attendance'),

]
