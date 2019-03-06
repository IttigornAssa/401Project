from django.db import models


class timeStamp(models.Model):

	datetime = models.DateTimeField(auto_now_add=True)

class cardRecord(models.Model):

	idCard=models.CharField(max_length=100)
	actionCard=models.CharField(max_length=50)
	descCard=models.CharField(max_length=400)
	commentCard=models.CharField(max_length=200)
	timestamp=models.ForeignKey(timeStamp,on_delete=models.CASCADE)


