from django.db import models
from django.db.models.signals import (
	pre_save,
	post_save
	)

from django.dispatch import receiver
from utilities.utils import category_slug_generator,item_slug_generator

# Create your models here.
class Categories(models.Model):
	Name=models.CharField(max_length=50)
	slug = models.SlugField(blank=True,null=True)
	def __str__(self):
		return str(self.Name)

class Item(models.Model):
	Name=models.CharField(max_length=50)
	Price=models.FloatField()
	Quantity=models.IntegerField()
	ShortDesc=models.TextField()
	LongDesc=models.TextField()
	Picture= models.ImageField(upload_to='images')
	Category = models.ForeignKey(Categories,on_delete=models.CASCADE)
	Stock=models.BooleanField(max_length=50, default=True)
	slug = models.SlugField(blank=True,null=True)

	def __str__(self):
		return str(self.Name)

@receiver(pre_save, sender=Categories)
def my_handler(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = item_slug_generator(instance)
		
class TT(models.Model):
	Name=models.CharField(max_length=800)
	def __str__(self):
		return str(self.Name)


@receiver(pre_save, sender=Categories)
def my_handler(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = category_slug_generator(instance)




