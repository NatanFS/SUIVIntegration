# Generated by Django 4.1.7 on 2023-03-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_comparisondata'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalspecsgroup',
            name='plate',
            field=models.CharField(max_length=7, null=True),
        ),
    ]