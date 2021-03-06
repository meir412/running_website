# Generated by Django 3.0.2 on 2020-01-11 15:18

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_sec', models.PositiveIntegerField()),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('route', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
            ],
        ),
    ]
