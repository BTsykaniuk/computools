from django.db import models
from django.contrib.postgres.fields import JSONField
from products.models import BaseModel, Item


class Order(BaseModel):
    """Moder for Orders"""

    PAYMENT_STATUS = (
        ('WAITING', 'Waiting'),
        ('SUCCESS', 'Success'),
        ('ERROR', 'Error'),
        ('CANCEL', 'Cancel'),
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_items_count = models.DecimalField(max_digits=6, decimal_places=0)
    status = models.CharField(max_length=7, choices=PAYMENT_STATUS)
    charge_id = models.CharField(max_length=30, blank=True)
    items = models.ManyToManyField(Item, through='OrderItem')
    metadata = JSONField(null=False, blank=True)

    def __str__(self):
        return f"Date - {self.create_date} Amount - {self.total_price}"

    class Meta:
        ordering = ['-create_date']


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order - {self.order}"
