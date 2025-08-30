from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CouponApplySerializer
from .models import Transaction, User
from django.conf import settings
import requests

@api_view(['POST'])
def apply_coupon(request):
    """API endpoint to apply a coupon and check for fraud"""
    print("=== APPLY COUPON REQUEST RECEIVED ===")  # Debug log
    print("Request data:", request.data)  # Debug log
    
    serializer = CouponApplySerializer(data=request.data)
    
    if not serializer.is_valid():
        print("Serializer errors:", serializer.errors)  # Debug log
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        data = serializer.validated_data
        print("Validated data:", data)  # Debug log
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=data['user_email'],
            defaults={'first_name': 'Guest', 'last_name': 'User'}
        )
        print("User:", user.email, "Created:", created)  # Debug log
        
        # Prepare data for ML service
        ml_data = {
            'user_id': str(user.id),
            'coupon_code': data['coupon_code'].code,
            'ip_address': data['ip_address'],
            'user_agent': data['user_agent']
        }
        print("Sending to ML service:", ml_data)  # Debug log
        
        try:
            # Call ML service for fraud prediction
            ml_response = requests.post(
                'http://localhost:8001/predict',
                json=ml_data,
                timeout=5
            )
            print("ML response status:", ml_response.status_code)  # Debug log
            print("ML response content:", ml_response.text)  # Debug log
            fraud_result = ml_response.json()
            
        except requests.exceptions.RequestException as e:
            print("ML service error:", str(e))  # Debug log
            # If ML service is down, proceed without fraud check
            fraud_result = {'fraud_probability': 0.0, 'is_fraud': False}
        
        # Create transaction record
        transaction = Transaction.objects.create(
            user=user,
            coupon=data['coupon_code'],
            original_amount=data['original_amount'],
            discounted_amount=data['original_amount'] * (1 - data['coupon_code'].discount_percent/100),
            ip_address=data['ip_address'],
            user_agent=data['user_agent'],
            device_fingerprint=f"hash_{data['ip_address']}_{data['user_agent']}",
            fraud_probability=fraud_result['fraud_probability'],
            is_fraud=fraud_result['is_fraud'],
            status='rejected' if fraud_result['is_fraud'] else 'approved'
        )
        print("Transaction created:", transaction.id)  # Debug log
        
        return Response({
            'success': not fraud_result['is_fraud'],
            'message': 'Fraud detected' if fraud_result['is_fraud'] else 'Coupon applied successfully',
            'discounted_amount': float(transaction.discounted_amount),
            'fraud_probability': float(fraud_result['fraud_probability'])
        })
    
    except Exception as e:
        print("Unexpected error:", str(e))  # Debug log
        return Response(
            {'message': 'Internal server error', 'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )