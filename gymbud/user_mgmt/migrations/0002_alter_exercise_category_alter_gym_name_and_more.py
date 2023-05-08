# Generated by Django 4.1.5 on 2023-05-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='category',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='gym',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='location',
            name='street',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='playlist',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]
