# Generated by Django 2.2 on 2021-10-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_timer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='date',
            field=models.CharField(max_length=100),
        ),
    ]
