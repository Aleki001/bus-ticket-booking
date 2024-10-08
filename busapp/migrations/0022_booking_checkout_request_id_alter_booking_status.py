# Generated by Django 5.1 on 2024-08-27 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0021_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]
