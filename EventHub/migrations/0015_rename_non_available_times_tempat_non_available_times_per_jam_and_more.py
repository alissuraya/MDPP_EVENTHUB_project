# Generated by Django 4.1.4 on 2024-02-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventHub', '0014_alter_nonavailabletime_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempat',
            old_name='non_available_times',
            new_name='non_available_times_per_jam',
        ),
        migrations.RemoveField(
            model_name='tempat',
            name='non_available_dates',
        ),
        migrations.AddField(
            model_name='tempat',
            name='non_available_dates_per_hari',
            field=models.ManyToManyField(related_name='tempat_non_available_per_hari', to='EventHub.nonavailabledate'),
        ),
        migrations.AddField(
            model_name='tempat',
            name='non_available_dates_per_jam',
            field=models.ManyToManyField(related_name='tempat_non_available_per_jam', to='EventHub.nonavailabledate'),
        ),
    ]
