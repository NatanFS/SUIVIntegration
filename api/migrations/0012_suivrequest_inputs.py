# Generated by Django 4.1.7 on 2023-03-17 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_equipment_is_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='suivrequest',
            name='inputs',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
