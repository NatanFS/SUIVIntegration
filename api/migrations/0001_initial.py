# Generated by Django 4.1.7 on 2023-03-14 20:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FipeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True)),
                ('fipe_id', models.IntegerField(null=True)),
                ('maker_description', models.CharField(max_length=255, null=True)),
                ('model_description', models.CharField(max_length=255, null=True)),
                ('version_description', models.CharField(max_length=255, null=True)),
                ('fuel', models.CharField(max_length=255, null=True)),
                ('current_value', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SUIVRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(max_length=255, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maker', models.CharField(max_length=255, null=True)),
                ('maker_id', models.IntegerField(null=True)),
                ('fipe_id', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('plate', models.CharField(max_length=255, null=True)),
                ('year_model', models.IntegerField(null=True)),
                ('year_fab', models.IntegerField(null=True)),
                ('fuel', models.CharField(max_length=255, null=True)),
                ('chassis', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('species', models.CharField(max_length=255, null=True)),
                ('bodywork', models.CharField(max_length=255, null=True)),
                ('power', models.IntegerField(null=True)),
                ('is_national', models.BooleanField(null=True)),
                ('axis_count', models.IntegerField(null=True)),
                ('total_gross_weight', models.FloatField(null=True)),
                ('maximum_traction_capacity', models.FloatField(null=True)),
                ('cc', models.IntegerField(null=True)),
                ('seat_count', models.IntegerField(null=True)),
                ('load_capacity', models.FloatField(null=True)),
                ('gear_box_number', models.CharField(max_length=255, null=True)),
                ('back_axis_count', models.CharField(max_length=255, null=True)),
                ('aux_axis_count', models.CharField(max_length=255, null=True)),
                ('engine_number', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuivData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fipe_id', models.IntegerField(null=True)),
                ('version_id', models.IntegerField(null=True)),
                ('version_description', models.CharField(max_length=255, null=True)),
                ('model_id', models.IntegerField(null=True)),
                ('model_description', models.CharField(max_length=255, null=True)),
                ('maker_id', models.IntegerField(null=True)),
                ('maker_description', models.CharField(max_length=255, null=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suiv_data', to='api.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_update', models.IntegerField(null=True)),
                ('year_update', models.IntegerField(null=True)),
                ('value', models.FloatField(null=True)),
                ('is_prediction', models.BooleanField(null=True)),
                ('fipe_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='api.fipedata')),
            ],
        ),
        migrations.AddField(
            model_name='fipedata',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fipe_data', to='api.vehicle'),
        ),
    ]