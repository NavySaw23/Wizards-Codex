# Generated by Django 5.1.1 on 2024-11-07 19:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_at_project_creator_alter_at_project_like_users_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pd_project',
            name='like_users',
        ),
        migrations.RemoveField(
            model_name='sdc_project',
            name='like_users',
        ),
        migrations.CreateModel(
            name='FlowerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AT_Project',
        ),
        migrations.DeleteModel(
            name='PD_Project',
        ),
        migrations.DeleteModel(
            name='SDC_Project',
        ),
    ]