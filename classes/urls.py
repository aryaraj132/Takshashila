from django.urls import path
from . import views

app_name = 'classes'
urlpatterns = [
    path('branch/',views.BranchListView.as_view(), name='branch_list'),
    path('branch/<slug:slug>/',views.SemesterListView.as_view(), name='semester_list'),
    path('branch/<str:branches>/<slug:slug>/',views.SubjectListsView.as_view(), name='subjects_list'),
    path('branch/<str:branches>/<str:semesters>/<slug:slug>',views.LessonListView.as_view(), name='lessons_list'),
    path('submission/<slug:slug>/',views.SubmissionCreateView.as_view(), name='submission'),
    path('submission/update/<slug:slug>/',views.SubmissionUpdateView.as_view(), name='submission_update'),
    path('submission/delete/<slug:slug>/',views.SubmissionDeleteView.as_view(), name='submission_delete'),
    path('assignments/',views.SubjectListView.as_view(), name='subject_assignment'),
    path('assignments/<slug:slug>',views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<slug:slug>/create/',views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<str:subject>/<slug:slug>',views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/<str:subject>/<slug:slug>/update/',views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<str:subject>/<slug:slug>/delete/',views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('',views.SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/create/',views.LessonCreateView.as_view(), name='lesson_create'),
    path('<slug:slug>/live',views.liveClass.as_view(), name='live_class'),
    path('<slug:slug>',views.LessonListView.as_view(), name='lesson_list'),
    path('<str:subjects>/<slug:slug>',views.LessonDetailView.as_view(), name='lesson_detail'),
    path('<str:subjects>/<slug:slug>/update/',views.LessonUpdateView.as_view(), name='lesson_update'),
    path('<str:subjects>/<slug:slug>/delete/',views.LessonDeleteView.as_view(), name='lesson_delete'),
]