# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import int_list_validator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    year_level = models.CharField(validators=[int_list_validator], max_length=7)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    max_capacity = models.IntegerField(validators=[MaxValueValidator(2)])

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])

    def __str__(self):
        return self.user.first_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name