# Generated by Django 4.2 on 2023-11-21 04:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_alter_project_description_alter_project_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AT_Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100)),
                ('like_count', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='img/projects')),
                ('description', models.CharField(default='Lorem', max_length=500)),
                ('like_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PD_Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100)),
                ('like_count', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='img/projects')),
                ('description', models.CharField(default='Lorem', max_length=500)),
                ('like_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SDC_Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100)),
                ('like_count', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='img/projects')),
                ('description', models.CharField(default='Lorem', max_length=500)),
                ('like_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]