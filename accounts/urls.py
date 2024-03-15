from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
path('', views.login_view , name = 'home'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('add_face/', views.add_face, name='add_face'),
path('search_attendance/', views.search_attendance, name='search_attendance'),
path('add_image/', views.add_image, name='add_image'),
]
