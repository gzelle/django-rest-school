# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.core.validators import int_list_validator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver

class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    year_level = models.CharField(validators=[int_list_validator], max_length=7)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    max_capacity = models.IntegerField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default="", related_name="students")
    classes = models.ManyToManyField('Class')
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.user.first_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.user.first_name