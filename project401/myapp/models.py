from django.db import models

# Create your models here.
class currentCard(models.Model):
	
	idCard=models.CharField(max_length=100)
	typeCard=models.CharField(max_length=50)
	date=models.CharField(max_length=50)
	currenttime=models.CharField(max_length=50)

class historyCard(models.Model):

	idCard=models.CharField(max_length=100)
	typeCard=models.CharField(max_length=50)
	compare =models.CharField(max_length=50) 
	date=models.CharField(max_length=50)
	currenttime=models.CharField(max_length=50)


