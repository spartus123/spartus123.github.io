# Generated by Django 4.2.6 on 2023-11-06 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_alter_customer_zipcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="phone",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="zipcode",
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
    ]
