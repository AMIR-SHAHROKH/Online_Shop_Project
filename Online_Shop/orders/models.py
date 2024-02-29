from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Order(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name}"
    
    def update_unit_price(self, *args, **kwargs):
        # Retrieve the product associated with the order item
        product = self.product

        # Set the unit price of the order item to the price of the product
        self.unit_price = product.price
        
        # Call the original save() method to save the order item
        super().save(*args, **kwargs)
    def calculate_total_price(self):
        """Calculate the total price for this order item."""
        return self.quantity * self.unit_price
    
class Discount(models.Model):

    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()
    def __str__(self):
        return self.name

class FinalAmount(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='final_amount')
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Final Amount - Order #{self.order.id}"
    
    def calculate_discounted_amount(self):
        # Retrieve the total amount from the associated order
        total_amount = self.order.total_amount
        
        # Retrieve the discount associated with the order
        discount = self.order.discount

        if discount:
            # Calculate the discounted amount based on the percentage
            discount_amount = (total_amount * discount.percentage) / 100
            
            # Ensure that the discount does not exceed $100
            if discount_amount > 100:
                raise ValidationError("Discount amount cannot exceed $100.")
            
            self.discounted_amount = total_amount - discount_amount
        else:
            # If there's no discount, set the discounted amount as the total amount
            self.discounted_amount = total_amount

        # Save the instance after calculating the discounted amount
        self.save()


@receiver(post_save, sender=FinalAmount)
def calculate_discounted_amount(sender, instance, created, **kwargs):
    if created:
        # Ensure the method runs only when the instance is created
        total_amount = instance.order.total_amount
        discount = instance.order.discount

        if discount:
            discount_amount = (total_amount * discount.percentage) / 100
            if discount_amount > 100:
                raise ValidationError("Discount amount cannot exceed $100.")
            
            instance.discounted_amount = total_amount - discount_amount
        else:
            instance.discounted_amount = total_amount

        # Modify the instance directly without saving it again
        FinalAmount.objects.filter(pk=instance.pk).update(discounted_amount=instance.discounted_amount)
