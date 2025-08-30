from django.db import models

# Core Model for storing User information
class User(models.Model):
    # Using Email as the primary identifier instead of default ID
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Hashed password will be stored here (for auth later)
    password_hash = models.CharField(max_length=255)
    # Timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

# Model to represent a unique discount coupon
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g., WELCOME20
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 20.00
    # Coupon can be valid only for a first-time order
    is_first_order_only = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)  # To enable/disable coupon
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

# THE CORE MODEL: Tracks every coupon application attempt
class Transaction(models.Model):
    # Link to the user who applied the coupon
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    # Link to the coupon that was applied
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='transactions')
    # Original order amount and final discounted amount
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # CRITICAL FRAUD DETECTION FIELDS
    ip_address = models.GenericIPAddressField()  # User's IP
    user_agent = models.TextField()  # Browser/device info
    # We will simulate device_id via a hash of user_agent + IP for this project
    device_fingerprint = models.CharField(max_length=255)
    
    # Result of the fraud check
    fraud_probability = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 0.87
    is_fraud = models.BooleanField(default=False)
    status_choices = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='under_review')
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This helps in quickly finding a user's transactions
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['device_fingerprint']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"Txn: {self.user.email} - {self.coupon.code} - {self.status}"