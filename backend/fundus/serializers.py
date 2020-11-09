from rest_framework import serializers
from .models import fundus

class fundusSerializer(serializers.ModelSerializer):
  class Meta:
    model = fundus
    fields = ('id','fundus_Img', 'title', 'path')