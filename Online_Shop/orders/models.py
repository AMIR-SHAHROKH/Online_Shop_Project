from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)



    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name}"
    
    def update_unit_price(self, *args, **kwargs):
        """Update the unit price based on the associated product's price and discount."""
        # Retrieve the product associated with the order item
        product = self.product

        # Calculate the unit price considering the discount if it exists
        if product.discount is not None and product.discount > 0:  # Check if discount is not None and greater than 0
            discounted_price = product.price * (1 - product.discount / 100)
            self.unit_price = discounted_price
        else:
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
    
    def calculate_discounted_amount(self, discount):
        # Retrieve the total amount from the associated order
        total_amount = self.order.total_amount
        
        # Calculate the discounted amount based on the selected discount and order's total amount
        if discount:
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
    def set_payment_status_paid(self):
        # Set the payment status of the associated order to 'paid'
        self.order.payment_status = FinalAmount.PAID
        self.order.save()

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
@receiver(post_save, sender=FinalAmount)
def update_order_payment_status(sender, instance, created, **kwargs):
    # Check if the payment status has been updated to 'paid'
    if instance.payment_status == FinalAmount.PAID:
        # Set the payment status of the associated order to 'paid'
        instance.set_payment_status_paid()