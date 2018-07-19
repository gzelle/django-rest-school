# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Subject, Class, Course, Student, Teacher

from django.contrib import admin

admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)