from django.db import models
from market.models import Order

# Create your models here.


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    username = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    paystack_ref = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self) -> str:
        return f"Payment made by {self.username}"
    
    def get_amount(self):
        return self.amount