# Generated by Django 5.0.6 on 2024-06-25 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0002_contact_facebook_contact_instagram_contact_tiktok_and_more'),
        ('core', '0006_tag_exported_tag_url_alter_allotment_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='veterinarian',
            name='pet',
        ),
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.address', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='emergency',
            field=models.BooleanField(default=True, verbose_name='Emergency'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='social',
            field=models.BooleanField(default=True, verbose_name='Social'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='tiktok',
            field=models.URLField(blank=True, null=True, verbose_name='Tiktok'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='twitter',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='veterinarian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care.veterinarian', verbose_name='Vet'),
        ),
        migrations.AlterField(
            model_name='veterinarian',
            name='doctor_crm',
            field=models.CharField(max_length=15, verbose_name='Dr. CRM'),
        ),
        migrations.AlterField(
            model_name='veterinarian',
            name='doctor_name',
            field=models.CharField(max_length=50, verbose_name='Dr. Name'),
        ),
        migrations.AlterField(
            model_name='veterinarian',
            name='hospital_name',
            field=models.CharField(max_length=50, verbose_name='Clinic name'),
        ),
    ]