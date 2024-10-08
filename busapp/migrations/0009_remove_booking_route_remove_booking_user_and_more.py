# Generated by Django 5.0.3 on 2024-08-09 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0008_bus_travel_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='route',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_id_number',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_name',
            field=models.CharField(default='user', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_phone',
            field=models.CharField(default=0, max_length=15),
        ),
        migrations.AddField(
            model_name='booking',
            name='seat_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='busapp.bus'),
        ),
    ]
