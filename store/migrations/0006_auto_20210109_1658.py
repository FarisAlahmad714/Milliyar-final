# Generated by Django 2.2 on 2021-01-10 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_shippingaddress_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='orderItem',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Product'),
        ),
    ]
