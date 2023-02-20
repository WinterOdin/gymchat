# Generated by Django 4.1.5 on 2023-02-18 13:51

import chat.models
from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DialogsModel',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
            ],
            options={
                'verbose_name': 'Dialog',
                'verbose_name_plural': 'Dialogs',
            },
        ),
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('-created',),
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=chat.models.user_directory_path, verbose_name='File')),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='Upload date')),
            ],
        ),
    ]
