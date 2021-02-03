# Generated by Django 2.2 on 2021-01-27 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=3)),
                ('dp', models.ImageField(blank=True, upload_to=users.models.imageUpload, verbose_name='dp')),
                ('user_type', models.CharField(choices=[('teacher', 'teacher'), ('student', 'student')], default='student', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
