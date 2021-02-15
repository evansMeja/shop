from django.db import models

# Create your models here.
class Categories(models.Model):
	Name=models.CharField(max_length=50)

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

	def __str__(self):
		return str(self.Name)
		
class TT(models.Model):
	Name=models.CharField(max_length=800)
	def __str__(self):
		return str(self.Name)

