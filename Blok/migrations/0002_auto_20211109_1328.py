# Generated by Django 3.1.5 on 2021-11-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blok', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_image',
            field=models.FileField(null=True, upload_to='avatars'),
        ),
    ]
