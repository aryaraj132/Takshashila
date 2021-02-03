from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, DetailView, ListView, FormView,CreateView,UpdateView,DeleteView)
from .models import Branch,Semester,Subject,Lesson
from .forms import LessonForm,CommentForm,ReplyForm
import os
from win32api import GetSystemMetrics
import numpy as np
import cv2
from mss import mss
# Create your views here.

class BranchListView(ListView):
    context_object_name = 'Branches'
    queryset = Branch.objects.all()
    template_name = 'classes/branch_list_view.html'
    
class SemesterListView(DetailView):
    context_object_name = 'Branches'
    model = Branch
    template_name = 'classes/semester_list_view.html'

class SubjectListView(ListView):
    context_object_name = 'Semesters'
    model = Semester
    template_name = 'classes/subject_list_view.html'

class SubjectListsView(DetailView):
    context_object_name = 'Semesters'
    model = Semester
    template_name = 'classes/subject_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'Subjects'
    model = Subject
    template_name = 'classes/lesson_list_view.html'

class LessonDetailView(DetailView, FormView):
    context_object_name = 'Lesson'
    model = Lesson
    template_name = 'classes/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_success_url(self):
        self.object = self.get_object()
        subject = self.object.subject
        return reverse_lazy('classes:lesson_detail',kwargs={'subjects':subject.slug,'slug':self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView,self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context
    
    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.form_class
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'
        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            return self.form2_valid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    
class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'subject'
    model = Subject
    template_name = 'classes/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('classes:lesson_list',kwargs={'slug' : self.object.slug})

    def form_valid(self, form,*args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','notes')
    model = Lesson
    template_name = 'classes/lesson_update.html'
    context_object_name = 'lesson'

class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'classes/lesson_delete.html'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse_lazy("classes:lesson_list", kwargs={"slug": self.object.subject.slug})

class liveClass(DetailView):
    context_object_name = 'Subjects'
    model = Subject
    template_name = 'classes/live_class.html'


def ScreenFeed(request):
    return StreamingHttpResponse(shareScreen(),content_type='multipart/x-mixed-replace; boundary=frame')

def shareScreen():
    mon = {'top': 0, 'left': 0, 'width': int(GetSystemMetrics(0)*1.25), 'height': int(GetSystemMetrics(1)*1.25)}
    with mss() as sct:
        while True:
            img = sct.grab(mon)
            ret, image = cv2.imencode('.jpg',np.array(img))
            yield (b'--frame\r\n'
                    b'Content-Type:image/jpeg\r\n\r\n'+image.tobytes()+b'\r\n\r\n')
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

def CamFeed(request):
    return StreamingHttpResponse(shareCamera(),content_type='multipart/x-mixed-replace; boundary=frame')

def shareCamera():
    camera = cv2.VideoCapture(0)
    camera.set(3, 1920)
    camera.set(4, 1080)
    while True:
        rtrn, frame=camera.read()
        cv2.imshow('camera', frame)
        ret, image = cv2.imencode('.jpg',frame)
        yield (b'--frame\r\n'
                b'Content-Type:image/jpeg\r\n\r\n'+image.tobytes()+b'\r\n\r\n')
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break