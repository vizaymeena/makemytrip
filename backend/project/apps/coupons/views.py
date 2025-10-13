from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Coupon
from .serializers import CouponSerializer, ApplyCouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD for coupons.
    """
    queryset = Coupon.objects.all().order_by('-valid_to')
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

    # Optional: list only active coupons for everyone
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def active(self, request):
        active_coupons = self.queryset.filter(active=True, valid_to__gte=timezone.now())
        serializer = self.get_serializer(active_coupons, many=True)
        return Response(serializer.data)


class ApplyCouponViewSet(viewsets.GenericViewSet):
    """
    Endpoint for users to validate/apply coupon at checkout.
    """
    serializer_class = ApplyCouponSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def apply(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)
