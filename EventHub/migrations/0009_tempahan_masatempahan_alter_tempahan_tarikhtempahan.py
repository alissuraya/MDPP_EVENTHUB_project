# Generated by Django 4.1.4 on 2024-02-18 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventHub', '0008_alter_tempahan_tarikhtempahan'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempahan',
            name='masaTempahan',
            field=models.TimeField(default='09:06'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tempahan',
            name='tarikhTempahan',
            field=models.DateField(auto_now_add=True),
        ),
    ]