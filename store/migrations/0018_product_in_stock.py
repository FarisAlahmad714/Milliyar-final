# Generated by Django 2.2 on 2021-10-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20211018_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
