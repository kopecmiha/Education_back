# Generated by Django 3.1.5 on 2021-11-09 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blok', '0003_auto_20211109_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FileField(null=True, upload_to='project_images'),
        ),
    ]
