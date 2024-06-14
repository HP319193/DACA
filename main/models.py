from django.db import models

class Image(models.Model):
    file = models.FileField(upload_to='source/')
    status = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)