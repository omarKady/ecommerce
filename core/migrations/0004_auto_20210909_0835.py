# Generated by Django 3.1 on 2021-09-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_order_ordered_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]