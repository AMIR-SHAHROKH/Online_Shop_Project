from django.db import models

# class TimeStampedModel(models.Model):
#     created_at = models.CharField(max_length=20, editable=False)
#     updated_at = models.CharField(max_length=20, editable=False)

#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         # Update the 'updated_at' timestamp before saving
#         self.updated_at = str(jdatetime_datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

#         if not self.created_at:
#             self.created_at = str(jdatetime_datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

#         super(TimeStampedModel, self).save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name}"

class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()
    def __str__(self):
        return self.name

class FinalAmount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)

