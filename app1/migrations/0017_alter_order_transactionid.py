# Generated by Django 5.0.7 on 2025-01-30 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0016_alter_order_product_alter_order_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transactionid",
            field=models.CharField(max_length=50),
        ),
    ]
