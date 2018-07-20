# Generated by Django 2.0.7 on 2018-07-20 13:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Create date')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Update date')),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Create date')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Update date')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=800)),
                ('active', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='products_images/')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
