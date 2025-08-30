from django.contrib import admin
from .models import User, Coupon, Transaction  # Import your models

# Register your models here so they appear in the admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_first_order_only', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_first_order_only')
    search_fields = ('code',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'status', 'fraud_probability', 'created_at')
    list_filter = ('status', 'is_fraud')
    search_fields = ('user__email', 'coupon__code')
