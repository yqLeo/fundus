from django.urls import path

from . import views
app_name = 'fundus'

urlpatterns = [
    path('path/', views.path, name='path'),
    path('upload/', views.upload, name='upload'),
]