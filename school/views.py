# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
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

    # List of students
    @action(detail=True)
    def students(self, request, pk=None, *args, **kwargs):
        this_class = self.get_object()
        students = this_class.student_set.all()
        serializer = StudentSerializer(students, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        this_class = self.get_object()
        serializer = ClassSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            teacher = serializer.validated_data['teacher']
            class_subject = serializer.validated_data['subject']
            subjects = teacher.subjects.get_queryset()
            for subject in subjects:
                if subject == class_subject:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_message = {"code": 400, "message": "{0} cannot be assigned to a class wherein the subject isn’t among the list of subjects he/she can teach.".format(teacher)}
        return Response(error_message, status=status.HTTP_200_OK)

class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request):
        serializer = StudentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            classes = serializer.validated_data['classes']
            year_level = serializer.validated_data['year_level']
            for this_class in classes:
                if int(year_level) == int(this_class.subject.year_level):
                    if int(this_class.student_set.all().count()) < int(this_class.max_capacity):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_message = {"code": 400, "message": "{0} already full.".format(this_class)}
        return Response(error_message, status=status.HTTP_200_OK)

class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer