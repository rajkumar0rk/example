# Generated by Django 3.1 on 2022-02-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220219_1655'),
        ('cart', '0002_auto_20220213_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
