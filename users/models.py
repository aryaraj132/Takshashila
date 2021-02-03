from django.db import models
from django.contrib.auth.models import User
import os
from classes.models import Branch,Semester 
# Create your models here.

def imageUpload(instance,filename):
    upload_to = 'Image/'
    ext = filename.split(".")[-1]
    if instance.user.username:
        filename = 'dp/{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    dp = models.ImageField(upload_to=imageUpload,verbose_name='dp', blank=True)

    teacher = 'teacher'
    student = 'student'
    user_types = [
        (teacher,'teacher'),
        (student,'student'),
    ]
    user_type = models.CharField(max_length = 10, choices = user_types,default=student)

    def __str__(self):
        return self.user.username