# Generated by Django 2.0.7 on 2018-07-25 09:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_item_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Create date')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Update date')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_items_count', models.DecimalField(decimal_places=0, max_digits=6)),
                ('status', models.CharField(choices=[('WAITING', 'Waiting'), ('SUCCESS', 'Success'), ('ERROR', 'Error')], max_length=7)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=None)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Create date')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Update date')),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=6)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='shopping.OrderItem', to='products.Item'),
        ),
    ]
