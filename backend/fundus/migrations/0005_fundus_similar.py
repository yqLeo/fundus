# Generated by Django 3.1.3 on 2021-01-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundus', '0004_fundus_analysis'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundus',
            name='similar',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]