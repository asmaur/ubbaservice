# Generated by Django 5.0.6 on 2024-06-22 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_petuuid_taguuid_rename_pet_uuid_pet_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taguuid',
            options={'managed': True, 'verbose_name': 'tag', 'verbose_name_plural': 'tags'},
        ),
    ]