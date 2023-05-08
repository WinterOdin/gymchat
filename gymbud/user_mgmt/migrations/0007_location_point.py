# Generated by Django 4.1.5 on 2023-05-05 14:01

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0006_alter_location_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]