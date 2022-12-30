
from email.policy import default
from select import select
from django.db import models

# Create your models here.









class DepartmentHead(models.Model):
    head_id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=100)
    head_name=models.CharField(max_length=200,null=True)
    head_mail=models.EmailField()
    head_password=models.CharField(max_length=100)
    status=models.IntegerField(default=0)
    def __str__(self):
        return self.department_name

  

class Department(models.Model):
    head_ids=models.ForeignKey(DepartmentHead,on_delete=models.CASCADE)
    department_name=models.CharField(max_length=200)
    department_email=models.EmailField()
    department_password=models.CharField(max_length=100)
    def __str__(self):
        return self.department_name



#creating verification acouts like vc registrar
verification_choices=[
    ('Varification','Varification'),('Non Varification','Non Varification')
]
class Main_accounts(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100,unique=True)
    varification_choices=models.CharField(max_length=100,choices = verification_choices,default=verification_choices[0])


    
