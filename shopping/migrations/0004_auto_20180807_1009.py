# Generated by Django 2.0.7 on 2018-08-07 10:09

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_auto_20180801_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]