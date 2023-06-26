from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Item(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='products')
    desc = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1, choices=STATUS)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("market:product", kwargs={"pk": self.pk})
    
    def get_add_to_cart_url(self):
        return reverse("market:add-to-cart", kwargs={"pk": self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse("market:emove-from-cart", kwargs={"pk": self.pk})
    


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_price(self):
        price = self.item.price
        total_price = price * self.quantity

        return total_price
    
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.id}"
    
    def get_total_price(self):

        total_price = 0
        order_items = self.items.filter(ordered=False)
        for item in order_items:
            total_price += item.get_total_price()
        
        return total_price
    

    class Meta:
        ordering = ['-created_on']