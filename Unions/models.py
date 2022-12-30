from django.db import models

# Create your models here.
class unions(models.Model):
    union_id=models.BigAutoField(primary_key=True)
    union_name=models.CharField(max_length=200)
    union_email=models.EmailField(unique=True)
    president_name=models.CharField(max_length=200)
    president_phone=models.IntegerField()
    secretary_name=models.CharField(max_length=200)
    secretary_phone=models.IntegerField()
    union_password=models.CharField(max_length=200)
    status=models.IntegerField(default=0)