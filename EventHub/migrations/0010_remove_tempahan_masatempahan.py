# Generated by Django 4.1.4 on 2024-02-18 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventHub', '0009_tempahan_masatempahan_alter_tempahan_tarikhtempahan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempahan',
            name='masaTempahan',
        ),
    ]
