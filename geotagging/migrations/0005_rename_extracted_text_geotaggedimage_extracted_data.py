# Generated by Django 5.0.7 on 2024-12-25 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geotagging', '0004_alter_geotaggedimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geotaggedimage',
            old_name='extracted_text',
            new_name='extracted_data',
        ),
    ]
