# Generated by Django 4.1.5 on 2023-05-05 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0005_alter_exercise_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(max_length=100),
        ),
    ]
