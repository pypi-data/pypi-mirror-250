from django.db import models

# Create your models here.

class maindata(models.Model):
    name = models.CharField(max_length=100)

class service(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class user(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class group(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class project(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
