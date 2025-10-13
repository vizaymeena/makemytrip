from django.db import models

# Create your models here.

from apps.common.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone



class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField( max_length=20, unique=True, help_text="Unique coupon code (case insensitive)" )

    discount_type = models.CharField( max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent' )

    discount_value = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Percentage (e.g., 10 for 10%) or Fixed amount (e.g., 100 for ₹100)" )

    min_spend = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True, help_text="Minimum purchase amount to apply coupon" )

    max_uses = models.PositiveIntegerField( default=1, help_text="Total number of times this coupon can be used globally" )

    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == 'percent' else '₹'})"

    def is_valid(self):
        """Check if coupon is still valid."""
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to and self.used_count < self.max_uses

    def apply_discount(self, total_amount):
        """Return discounted amount after applying coupon."""
        if not self.is_valid():
            return total_amount  # No discount if coupon invalid
        if self.discount_type == 'percent':
            discount = (total_amount * self.discount_value) / 100
        else:
            discount = self.discount_value
        return max(total_amount - discount, 0)

    class Meta:
        ordering = ['-valid_to']
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'


class CouponUsage(models.Model):
    """Tracks which user used which coupon and when."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    used_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coupon')  # prevent multiple use by same user
        verbose_name = 'Coupon Usage'
        verbose_name_plural = 'Coupon Usages'

    def __str__(self):
        return f"{self.user.username} used {self.coupon.code} on {self.used_on.strftime('%Y-%m-%d')}"
