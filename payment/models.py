from django.db import models
from django.conf import settings
from insurance.models import PolicyApplication

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    policy_application = models.ForeignKey(PolicyApplication, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f'Payment {self.transaction_id} by {self.user.username}'

class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_methods")
    method_type = models.CharField(max_length=50)  # e.g., "Credit Card", "Debit Card"
    card_number = models.CharField(max_length=19)
    card_holder_name = models.CharField(max_length=50)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    cvc = models.CharField(max_length=3)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.method_type} - {self.card_holder_name}'
