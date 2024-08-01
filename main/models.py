from django.db import models

class Image(models.Model):
    file = models.FileField(upload_to='source/')
    status = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    processId = models.CharField(max_length=40)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Process(models.Model):
    processId = models.CharField(max_length=40)
    datetime = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=255)

class Users(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    useremail = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_type = models.IntegerField(default=0)