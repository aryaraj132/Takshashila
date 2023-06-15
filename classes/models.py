import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import os
# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Semester(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='semester')
    def __str__(self):
        return self.name + "_" + self.branch.name
    
    class Meta:
        unique_together = ('name', 'branch',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

def subject_image(instance,filename):
    upload_to = 'Image/'
    ext = filename.split(".")[-1]
    if instance.subject_id:
        filename = 'Subject_Images/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subject')
    image = models.ImageField(upload_to=subject_image,blank=True,verbose_name='Subject Image')

    def __str__(self):
        return self.subject_id
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args,**kwargs)

def lesson_files(instance,filename):
    ext = filename.split(".")[-1]
    if instance.lesson_id:
        filename = 'Lesson_files/{}/{}.{}'.format(instance.subject.slug,instance.lesson_id, ext)
    return filename

class Lesson(models.Model):
    lesson_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Lecture Number")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=lesson_files,verbose_name="Video", blank=True,null=True)
    notes = models.FileField(upload_to=lesson_files,verbose_name="Notes", blank=True,null=True)
    ppt = models.FileField(upload_to=lesson_files,verbose_name="Presentation", blank=True,null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+"-"+str(self.semester.slug))
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("classes:lesson_list", kwargs={"slug": self.subject.slug})

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson,null=True,on_delete=models.CASCADE,related_name='comments')
    com_name = models.CharField(max_length=100,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.com_name = slugify("comment by"+"-"+str(self.author)+str(self.date_added))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.com_name
    
    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    reply_body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'reply to' + str(self.comment_name.com_name)

def assignment_files(instance,filename):
    ext = filename.split(".")[-1]
    if instance.assignment_id:
        filename = 'assignment_files/{}/{}.{}'.format(instance.subject.slug,instance.assignment_id, ext)
    return filename

class Assignment(models.Model):
    assignment_id = models.CharField(max_length=100,unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignment')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_date = models.DateField(auto_now_add=False, blank=True,null=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500,blank=True)
    position = models.PositiveSmallIntegerField(verbose_name="Assignment Number")
    slug = models.SlugField(null=True, blank=True)
    file = models.FileField(upload_to=assignment_files,verbose_name="Files", blank=True,null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.assignment_id)
        super().save(*args,**kwargs)
def submission_files(instance,filename):
    ext = filename.split(".")[-1]
    if instance.submission_id:
        filename = 'assignment_files/{}/{}/{}.{}'.format(instance.assignment.subject.slug,instance.assignment.assignment_id, instance.submission_id, ext)
    return filename

class Submission(models.Model):
    submission_id = models.CharField(max_length=100,unique=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submission')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500,blank=True)
    slug = models.SlugField(null=True, blank=True)
    ans_file = models.FileField(upload_to=submission_files,verbose_name="Files", blank=True,null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.submission_id)
        super().save(*args,**kwargs)
