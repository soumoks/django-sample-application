# Generated by Django 3.0.4 on 2020-03-27 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0002_auto_20200326_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='sex',
            field=models.CharField(choices=[(1, 'M'), (2, 'F')], max_length=1),
        ),
    ]
