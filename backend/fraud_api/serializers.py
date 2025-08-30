from rest_framework import serializers
from .models import Transaction, Coupon, User

class CouponApplySerializer(serializers.Serializer):
    """Serializer for applying a coupon"""
    coupon_code = serializers.CharField(max_length=20)
    user_email = serializers.EmailField()
    original_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    ip_address = serializers.IPAddressField()
    user_agent = serializers.CharField()

    def validate_coupon_code(self, value):
        """Check if coupon exists and is active"""
        try:
            coupon = Coupon.objects.get(code=value, is_active=True)
            return coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired coupon code.")