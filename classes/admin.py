from django.contrib import admin
from classes.models import Branch,Semester,Subject,Lesson,Comment,Reply
# Register your models here.
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)