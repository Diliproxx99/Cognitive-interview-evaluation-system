from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('upload/', views.resume_upload, name='resume_upload'),

    path('analyze/', views.analyze_resume, name='analyze_resume'),
    
    path("setup/", views.interview_setup, name="interview_setup"),
    path("interview/start/", views.start_interview, name="start_interview"),
    path("interview/question/", views.interview_question, name="interview_question"),
    path("interview/complete/", views.interview_complete, name="interview_complete"),
    path('countdown/', views.countdown, name='countdown')

]