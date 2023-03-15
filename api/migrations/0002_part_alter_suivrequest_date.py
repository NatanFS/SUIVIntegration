# Generated by Django 4.1.7 on 2023-03-15 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fipe_id', models.IntegerField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('nickname_id', models.IntegerField(null=True)),
                ('nickname_description', models.CharField(max_length=255, null=True)),
                ('complement', models.CharField(max_length=255, null=True)),
                ('part_number', models.CharField(max_length=255, null=True)),
                ('is_genuine', models.BooleanField(null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('aftermarket_maker_description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='suivrequest',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
