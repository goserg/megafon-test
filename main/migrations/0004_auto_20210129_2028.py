# Generated by Django 3.1.5 on 2021-01-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210129_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
