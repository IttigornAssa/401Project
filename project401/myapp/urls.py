from rest_framework import routers
from myapp.viewsets import changeReqViewSet

router = routers.DefaultRouter()
router.register(r'changeReq', changeReqViewSet)