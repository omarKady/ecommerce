# Generated by Django 3.1 on 2021-09-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_feedback_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered_quantity',
            field=models.PositiveIntegerField(default=None),
        ),
    ]