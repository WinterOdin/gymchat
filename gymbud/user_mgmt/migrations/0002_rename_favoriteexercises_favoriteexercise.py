# Generated by Django 4.1.5 on 2023-03-16 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteExercises',
            new_name='FavoriteExercise',
        ),
    ]
