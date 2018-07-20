from django.db import models
from django.contrib.postgres.fields import JSONField



class Date(models.Model):
    create_date = models.DateField('Create date', auto_now_add=True)
    update_date = models.DateField('Update date', auto_now=True)

    class Meta:
        abstract = True


class Product(Date):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=800)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='static/products_images/')

    def __str__(self):
        return f'{self.name}'


class Item(Date):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    metadata = JSONField(blank=True, default=None)

    def __str__(self):
        return f'{self.name} item'
