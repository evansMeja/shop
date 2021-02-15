from django.db import models
from superuser.models import Item, Categories
from django.contrib.auth.models import User

class cart(models.Model):
	sessionid=models.CharField(max_length=60, null=True)
	itemname=models.CharField(max_length=60,blank=True,null=True)
	itemprice=models.CharField(max_length=60,blank=True,null=True)
	actualitem=models.ForeignKey(Item,on_delete=models.CASCADE,default=1)

class order(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    callnumber=models.CharField(max_length=60,blank=True,null=True)
    counter=models.CharField(max_length=60,blank=True,null=True)
    is_delivered=models.BooleanField(default=False)
    subtotal= models.FloatField(default=0.0)
    
class cartitemdetail(models.Model):
	owner = models.ForeignKey(order,on_delete=models.CASCADE,default=1)
	Name=models.CharField(max_length=50,blank=True,null=True)
	Price=models.FloatField(default=0.0)
	Quantity=models.IntegerField(blank=True,null=True)
	ShortDesc=models.TextField(blank=True,null=True)
	LongDesc=models.TextField(blank=True,null=True)
	Picture= models.ImageField(upload_to='images',default='/media/c/1.jpg')
	Category = models.ForeignKey(Categories,on_delete=models.CASCADE,default=1)
	Stock=models.BooleanField(max_length=50, default=True)
	
class mailings(models.Model):
	email=models.CharField(max_length=50)

# Create your models here.
