from rest_framework import serializers
from django.utils import timezone
from .models import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'discount_type', 'discount_value', 'min_spend',
            'max_uses', 'used_count', 'valid_from', 'valid_to', 'active'
        ]
        read_only_fields = ['used_count']

    def validate(self, data):
        valid_from = data.get('valid_from')
        valid_to = data.get('valid_to')
        discount_value = data.get('discount_value')
        discount_type = data.get('discount_type')

        if valid_from and valid_to and valid_to <= valid_from:
            raise serializers.ValidationError("valid_to must be later than valid_from.")

        if discount_type == 'percent' and (discount_value <= 0 or discount_value > 100):
            raise serializers.ValidationError("Percentage discount must be between 1 and 100.")

        if discount_type == 'fixed' and discount_value <= 0:
            raise serializers.ValidationError("Fixed discount must be greater than 0.")

        return data


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        request = self.context.get('request')
        user = request.user 

        code = data['code'].strip().upper() # upper case after removing whitespaces
        total_amount = data['total_amount']

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid coupon code."})

        # 1. Check if active and within date range
        now = timezone.now()
        if not coupon.active:
            raise serializers.ValidationError({"code": "This coupon is inactive."})
        if not (coupon.valid_from <= now <= coupon.valid_to):
            raise serializers.ValidationError({"code": "This coupon is expired or not yet valid."})

        # 2. Check global usage limit
        if coupon.used_count >= coupon.max_uses:
            raise serializers.ValidationError({"code": "This coupon has reached its usage limit."})

        # 3. Check per-user usage (if user is logged in)
        if user and CouponUsage.objects.filter(user=user, coupon=coupon).exists():
            raise serializers.ValidationError({"code": "You have already used this coupon."})

        # 4. Check minimum spend
        if coupon.min_spend and total_amount < coupon.min_spend:
            raise serializers.ValidationError(
                {"code": f"Minimum spend of ₹{coupon.min_spend} required to use this coupon."}
            )

        # All validations passed — attach coupon object to validated data
        data['coupon'] = coupon
        return data

    def create(self, validated_data):
        """
        Register coupon usage and return the new discounted total.
        """
        request = self.context.get('request')
        user = request.user 
        coupon = validated_data['coupon']
        total_amount = validated_data['total_amount']

        # Apply discount
        discounted_total = coupon.apply_discount(total_amount)

        # Record usage if applicable
        if user:
            CouponUsage.objects.create(user=user, coupon=coupon)

        # Increment global usage count
        coupon.used_count += 1
        coupon.save(update_fields=['used_count'])

        return {
            "original_total": total_amount,
            "discounted_total": discounted_total,
            "discount_applied": total_amount - discounted_total,
            "coupon_code": coupon.code,
            "message": f"Coupon '{coupon.code}' applied successfully!"
        }
