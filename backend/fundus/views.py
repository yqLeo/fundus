# coding=utf-8
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
    output = subprocess.check_output("cd /home/qianyulong01/server/baidu/AIIB-MIA/retina-paddle-deploy && CUDA_VISIBLE_DEVICES=2, python -m retina_paddle_deploy.ai_retina " + path + " right CU_V", shell=True)
    result2 = output.decode(encoding="utf8")
    pathinfo.title = result
    pathinfo.analysis = result2
    pathinfo.save()
    return HttpResponse("http://localhost:3000/")

@csrf_exempt
def upload(request):
    title = request.FILES['image']
    if fundus.objects.filter(path=str(title)).exists():
        return HttpResponse("http://localhost:3000/")
    pathinfo = fundus()
    pathinfo.title = "..processing......"
    pathinfo.analysis = "..processing......"
    pathinfo.similar = "..processing......"
    pathinfo.path = str(title) 
    pathinfo.fundus_Img = title
    pathinfo.save()
    cur = fundus.objects.get(path=str(title))
    path = "/Users/leoqian/Desktop/cheetah/Website/fundus/backend/images/images/" + str(title)
    result = subprocess.check_output("python camera_classify.py " + path, shell=True)
    cur.title = result
    cur.save()
    #output = subprocess.check_output("cd /home/qianyulong01/server/baidu/AIIB-MIA/retina-paddle-deploy && CUDA_VISIBLE_DEVICES=2, python -m retina_paddle_deploy.ai_retina " + path + " right CU_V", shell=True)
    #result2 = output.decode(encoding="utf8")
    #cur.analysis = result2
    #cur.save()
    #result3 = subprocess.check_output("python top_k_similar.py " + path + " 5", shell=True)
    #cur.similar = result3
    #cur.save()
    return HttpResponse("http://localhost:3000/")

class fundusView(viewsets.ModelViewSet):       # add this
  serializer_class = fundusSerializer          # add this
  queryset = fundus.objects.all()              # add this
 
  
