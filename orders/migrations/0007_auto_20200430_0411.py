# Generated by Django 3.0.5 on 2020-04-30 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_is_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('special_status', 'Can check all orders')]},
        ),
    ]