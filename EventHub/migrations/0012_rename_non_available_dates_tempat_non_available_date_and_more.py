# Generated by Django 4.1.4 on 2024-02-18 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventHub', '0011_nonavailabletime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempat',
            old_name='non_available_dates',
            new_name='non_available_date',
        ),
        migrations.RemoveField(
            model_name='tempat',
            name='non_available_times',
        ),
        migrations.RemoveField(
            model_name='tempahan',
            name='selectedTime',
        ),
        migrations.DeleteModel(
            name='NonAvailableTime',
        ),
        migrations.AddField(
            model_name='tempahan',
            name='selectedTime',
            field=models.CharField(blank=True, default='-', max_length=100, null=True),
        ),
    ]