from rest_framework import viewsets
from .serializers import changeReqSerializer
from .models import changeReq

class changeReqViewSet(viewsets.ModelViewSet):
    queryset = changeReq.objects.all()
    serializer_class = changeReqSerializer


