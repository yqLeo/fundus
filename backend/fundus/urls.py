from django.urls import path

from . import views
app_name = 'fundus'

urlpatterns = [
    # ex: /polls/5/
    path('path/', views.path, name='path'),
    
]