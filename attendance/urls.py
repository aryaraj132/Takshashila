from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='attendance'),
    path('test',views.test,name='test'),
    path('dataset',views.face,name='dataset'),
    path('mark_atnd',views.mark,name='mark_atnd'),
    path('show_msg',views.showMsg,name='show_msg'),
    path('stream',views.stream,name='stream'),
    path('make_dataset',views.dataset,name='make_dataset'),
    path('train_dataset',views.train,name='train_dataset'),
    path('show_attendance',views.showAttendance,name='show_attendance'),
]