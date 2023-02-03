# Generated by Django 4.1.5 on 2023-01-25 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='playlist',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='swipes_left',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='swipes_right',
            field=models.PositiveIntegerField(null=True),
        ),
    ]