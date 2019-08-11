"""InfoManagingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from app.views import *

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/', loginpage, name='loginpage'),
    url(r'^password/', passwordpage, name='password'),
    url(r'^logout/', logout, name='logout'),
    url(r'^tutor/', tutorpage, name='tutorpage'),
    url(r'^edit-tutor/(\S+)/', edit_tutor, name='edit_tutor'),
    url(r'^delete-tutor/(\S+)/', delete_tutor, name='delete_tutor'),
    url(r'^teacher/', teacherpage, name='teacherpage'),
    url(r'^edit-teacher/(\S+)/', edit_teacher, name='edit_teacher'),
    url(r'^delete-teacher/(\S+)/', delete_teacher, name='delete_teacher'),
    url(r'^course/', coursepage, name='coursepage'),
    url(r'^edit-course/(\S+)/', edit_course, name='edit_course'),
    url(r'^course-teacher/(\S+)/', course_teacher, name='course_teacher'),
    url(r'^delete-course-teacher/(\S+)/(\S+)/', delete_course_teacher, name='delete_course_teacher'),
    url(r'^delete-course/(\S+)/', delete_course, name='delete_course'),
    url(r'^student/', studentpage, name='studentpage'),
    url(r'^edit-student/(\S+)/', edit_student, name='edit_student'),
    url(r'^delete-student/(\S+)/', delete_student, name='delete_student'),
    url(r'^delete-select/(\S+)/(\S+)/', delete_select, name='delete_select'),
    url(r'^add-time/(\S+)/(\S+)/', add_time, name='add_time'),
    url(r'^sub-time/(\S+)/(\S+)/', sub_time, name='sub_time'),
    url(r'^class/(\S+)/', classpage, name='classpage'),
    url(r'^edit-class/(\S+)/', edit_class, name='edit-class'),
    url(r'^delete-class/(\S+)/', delete_class, name='delete-class'),
    url(r'^add-teacher-time/(\S+)/', add_teacher_time, name='add_teacher_time'),
    url(r'^sub-teacher-time/(\S+)/', sub_teacher_time, name='sub_teacher_time'),
    url(r'^teacher-record/(\S+)/', teacherrecordpage, name='teacherrecordpage'),
    url(r'^edit-teacher-record/(\S+)/', edit_teacher_record, name='edit_teacher_record'),
    url(r'^delete-teacher-record/(\S+)/', delete_teacher_record, name='delete_teacher_record'),
]
