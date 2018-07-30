from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers
from .models import Subject, Class, Course, Student, Teacher


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('url', 'id', 'name', 'code', 'year_level')

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ('url', 'id', 'name', 'max_capacity', 'subject', 'teacher', 'student_count')

    # Show student count
    def get_student_count(self, instance):
        return instance.student_set.all().count()

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    student_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        subjects = SubjectSerializer()
        students = serializers.SerializerMethodField()
        fields = ('url', 'id', 'name', 'code', 'subjects', 'students', 'student_count', 'teacher_count')

    def get_students(self, instance):
        names = []
        students = instance.students.get_queryset()
        for i in students:
            names.append(i.user.first_name)
        return names

    def get_student_count(self, instance):
        return instance.students.get_queryset().count()

    def get_teacher_count(self, instance):
        subjects = instance.subjects.get_queryset()
        return subjects.aggregate(Count('teacher'))['teacher__count']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name')

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        user = UserSerializer()
        course = CourseSerializer()
        subjects = SubjectSerializer()
        classes = ClassSerializer()
        fields = ('url', 'id', 'user', 'year_level', 'course', 'subjects', 'classes')

class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        user = UserSerializer()
        subjects = SubjectSerializer()
        fields = ('url', 'id', 'user', 'subjects')

