# Generated by Django 3.0.4 on 2020-04-02 00:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_type', models.CharField(choices=[('One-Way', 'One-Way'), ('Round-Trip', 'Round-Trip')], default='One-Way', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_desc', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Food_Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default=None, max_length=100)),
                ('model_no', models.PositiveIntegerField(default=None)),
                ('capacity', models.PositiveIntegerField(default=None)),
                ('max_row', models.PositiveIntegerField(default=None)),
                ('max_col', models.PositiveIntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_city', models.CharField(default=None, max_length=30)),
                ('arrival_city', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('arrival_time', models.TimeField(default=None)),
                ('departure_time', models.TimeField(default=None)),
                ('plane_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Plane')),
                ('route_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Route')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(default=None, max_length=30)),
                ('lname', models.CharField(default=None, max_length=30)),
                ('age', models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(0, 'Please enter correct value'), django.core.validators.MaxValueValidator(100, 'Please enter correct value')])),
                ('sex', models.CharField(choices=[('M', 'M'), ('F', 'F')], default='M', max_length=1)),
                ('seat_number', models.CharField(default=None, max_length=4)),
                ('food_name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Food_Name')),
            ],
        ),
        migrations.CreateModel(
            name='Feature_Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Feature')),
                ('plane_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Plane')),
            ],
        ),
        migrations.CreateModel(
            name='Booking_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Booking')),
                ('passenger_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Passenger')),
                ('trip_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Trip')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='passenger_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Passenger'),
        ),
        migrations.AddField(
            model_name='booking',
            name='trip_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Trip'),
        ),
    ]
