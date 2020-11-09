from django.db import models

# Create your models here.

# add this
class fundus(models.Model):
  fundus_Img = models.ImageField(upload_to='images/', blank=True, null=True) 
  title = models.CharField(max_length=120)
  path = models.TextField()

  def _str_(self):
    return self.title