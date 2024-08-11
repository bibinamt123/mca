from django.db import models
import uuid

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=100)  

    def __str__(self):
        return self.username

class Employee(models.Model):
    emp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_name = models.CharField(max_length=200)
    emp_password = models.CharField(max_length=100) 

    def __str__(self):
        return self.emp_name

class Order(models.Model):
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    order_status = models.CharField(max_length=200)

    def __str__(self):
        return f"Order {self.order_id} by {self.user_id}"

class Product(models.Model):
    pro_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    des = models.CharField(max_length=300)
    image = models.ImageField(upload_to='profile_pics/') 
    price = models.IntegerField() 

    def __str__(self):
        return self.name

class Feedback(models.Model):
    rep_id = models.CharField(primary_key=True, max_length=100)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)

    def __str__(self):
        return f"Feedback by {self.emp_id}"
