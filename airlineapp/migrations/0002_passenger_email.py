# Generated by Django 3.0.4 on 2020-04-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
