# Generated by Django 3.1.2 on 2020-11-04 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fundus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundus',
            name='fundus_Img',
        ),
    ]