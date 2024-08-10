from django.db import models

# Create your models here.
class User(models.Model):
  username=models.CharField(max_length=200),
  password=models.IntegerField(max_length=10),
  
class Employee(models.Model):
  emp_id=models.UUIDField(primary_key= True,unique=True),
  emp_name=models.CharField(max_length=200),
  emp_password=models.IntegerField(max_length=10),
  
class Order(models.Model):
  order_id=models.CharField(max_length=100.models,null=True),
  user_id=models.ForeignKey(Employee,on_delete=models.CASCADE),
  order_status=models.CharField(max_length=200),
  
class Product(models.Model):
  pro_id=models.CharField(max_length=200,primary_key=True),
  name=models.CharField(max_length=200),
  des=models.CharField(max_length=300),
  image=models.ImageField(models.ImageField(upload_to='profile_pics/')),
  price=models.IntegerField(max_length=200)
  
class Feedback(models.Model):
  rep_id=models.CharField(primary_key=True),
  emp_id=models.ForeignKey(Employee,max_length=200),
  feedback=models.CharField(max_length=200)