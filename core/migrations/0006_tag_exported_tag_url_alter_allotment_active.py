# Generated by Django 5.0.6 on 2024-06-25 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_taguuid_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='exported',
            field=models.BooleanField(default=False, verbose_name='Exported'),
        ),
        migrations.AddField(
            model_name='tag',
            name='url',
            field=models.URLField(default='', verbose_name='tag url'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allotment',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
    ]
