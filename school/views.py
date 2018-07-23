# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Subject, Class, Course, Student, Teacher
from .serializers import SubjectSerializer, ClassSerializer, CourseSerializer, StudentSerializer, TeacherSerializer, UserSerializer

from django.shortcuts import render

class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=True)
    def teachers(self, request, pk=None, *args, **kwargs):
        subject = self.get_object()
        teachers = subject.teacher_set.all()
        serializer = TeacherSerializer(teachers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def courses(self, request, pk=None, *args, **kwargs):
        subject = self.get_object()
        courses = subject.course_set.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)

class ClassView(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    @action(detail=True)
    def students(self, request, pk=None, *args, **kwargs):
        this_class = self.get_object()
        students = this_class.student_set.all()
        serializer = StudentSerializer(students, many=True, context={'request': request})
        return Response(serializer.data)

class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer