from .models import changeReq
from rest_framework import serializers

class changeReqSerializer(serializers.ModelSerializer):
	class Meta:
		model = changeReq
		fields = ('amountChange','timestamp')
		#fields = '__all__'
