# Generated by Django 3.1.2 on 2020-11-04 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundus', '0002_remove_fundus_fundus_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundus',
            name='fundus_Img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
