# Generated by Django 3.1.4 on 2020-12-21 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201220_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='customer_id',
            field=models.CharField(default='44uqbxsknmjkh14o5gdz', max_length=20),
        ),
    ]
