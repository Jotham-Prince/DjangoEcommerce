# Generated by Django 5.0.2 on 2024-05-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoEcommerceApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='profile_pic',
            field=models.ImageField(default='', upload_to=''),
        ),
        migrations.AlterField(
            model_name='merchantuser',
            name='profile_pic',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
