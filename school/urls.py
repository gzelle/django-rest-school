from django.conf.urls import url, include
from django.contrib import admin
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('subjects', views.SubjectView)
router.register('classes', views.ClassView)
router.register('courses', views.CourseView)
router.register('users', views.UserView)
router.register('students', views.StudentView)
router.register('teachers', views.TeacherView)

urlpatterns = [
    url('', include(router.urls))
]
