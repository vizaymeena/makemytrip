
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.coupons.views import *

router = DefaultRouter()
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'apply-coupon', ApplyCouponViewSet, basename='apply-coupon')

urlpatterns = [
    path('api/coupons/',include(router.urls)),
]