from django.db import models


# class currentCard2(models.Model):
	
# 	idCard=models.CharField(max_length=100)
# 	typeCard=models.CharField(max_length=50)
# 	descCard = models.CharField(max_length=500)
# 	date=models.CharField(max_length=50)
# 	currenttime=models.CharField(max_length=50)

# class historyCard2(models.Model):

# 	idCard=models.CharField(max_length=100)
# 	typeCard=models.CharField(max_length=50)
# 	descCard = models.CharField(max_length=500)
# 	compare =models.CharField(max_length=50) 
# 	date=models.CharField(max_length=50)
# 	currenttime=models.CharField(max_length=50)


class timeStamp(models.Model):
	
	dates=models.CharField(max_length=50)
	times=models.CharField(max_length=50)

class cardRecord(models.Model):

	idCard=models.CharField(max_length=100)
	actionCard=models.CharField(max_length=50)
	timestampID=models.CharField(max_length=50)


