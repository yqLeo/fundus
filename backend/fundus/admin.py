from django.contrib import admin
from .models import fundus # add this
# Register your models here.
class fundusAdmin(admin.ModelAdmin):  # add this
  list_display = ('fundus_Img','title','path','analysis','similar') # add this

# Register your models here.
admin.site.register(fundus, fundusAdmin) # add this