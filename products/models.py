from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify


class BaseModel(models.Model):
    create_date = models.DateField('Create date', auto_now_add=True)
    update_date = models.DateField('Update date', auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=800)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products_images/')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class Item(BaseModel):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, related_name='items')
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    metadata = JSONField(default=None, null=True)

    def __str__(self):
        return f'{self.name} item'

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.active = False

        return super(Item, self).save(*args, **kwargs)

