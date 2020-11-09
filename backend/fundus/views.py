from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files.base import ContentFile
from io import BytesIO
# Create your views here.
from rest_framework import viewsets          # add this
from .serializers import fundusSerializer      # add this
from .models import fundus                     # add this
import json
import subprocess
from PIL import Image
import os


@csrf_exempt
def path(request):
    pathinfo = fundus()
    path = json.loads(request.body.decode('utf-8'))['path']
    os.system("cp "+path+ " ./image")
    name = os.path.basename(path)
    im = Image.open("image/"+name)
    im.thumbnail((220, 130), Image.ANTIALIAS)
    thumb_io = BytesIO()
    im.save(thumb_io, im.format, quality=60)
    pathinfo.fundus_Img.save(im.filename, ContentFile(thumb_io.getvalue()), save=False)
    
    pathinfo.path = path
    result = subprocess.check_output("python camera_classify.py " + path, shell=True)
    pathinfo.title = result
    pathinfo.save()
    return HttpResponse("http://localhost:3000/")

class fundusView(viewsets.ModelViewSet):       # add this
  serializer_class = fundusSerializer          # add this
  queryset = fundus.objects.all()              # add this
 
  
