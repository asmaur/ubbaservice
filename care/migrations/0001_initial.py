# Generated by Django 5.0.6 on 2024-06-22 10:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('icon', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='')),
                ('description', models.CharField(max_length=255, verbose_name='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allergies', to='core.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet')),
            ],
            options={
                'verbose_name': 'Health',
                'verbose_name_plural': 'Healths',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Behavior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='')),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care.health', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Medecine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('unit', models.CharField(max_length=15)),
                ('instruction', models.TextField()),
                ('caution', models.TextField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medecines', to='core.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care.health')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('icon', models.CharField(blank=True, max_length=10, null=True)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('is_default', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='care.category')),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='')),
                ('health', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='care.health')),
            ],
        ),
        migrations.CreateModel(
            name='Veterinarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=50, verbose_name='')),
                ('hospital_name', models.CharField(max_length=50, verbose_name='')),
                ('doctor_crm', models.CharField(max_length=15, verbose_name='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='')),
                ('lot', models.CharField(max_length=50, verbose_name='')),
                ('injection_date', models.DateField(verbose_name='')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet')),
                ('veterinary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='care.veterinarian')),
            ],
            options={
                'verbose_name': 'Vaccine',
                'verbose_name_plural': 'Vaccines',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_visit', models.TextField(verbose_name='Reason for visit/ Diagnosis')),
                ('diagnosis', models.TextField(verbose_name='Assesment/ Diagnosis')),
                ('treatment', models.TextField(verbose_name='Treatment/ Recommendation')),
                ('initial_date', models.DateField(verbose_name='')),
                ('final_date', models.DateField(verbose_name='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='core.pet', verbose_name='')),
                ('veterinary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='care.veterinarian', verbose_name='')),
            ],
            options={
                'verbose_name': 'Treatment',
                'verbose_name_plural': 'Treatments',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('phone', models.CharField(max_length=50, verbose_name='')),
                ('social', models.BooleanField(default=True, verbose_name='')),
                ('emergency', models.BooleanField(default=False, verbose_name='')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.address', verbose_name='')),
                ('veterinarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care.veterinarian', verbose_name='')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'db_table': '',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Weigh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(verbose_name='')),
                ('unit', models.CharField(max_length=5, verbose_name='')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
                'db_table': '',
                'managed': True,
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='care_record_content_4b62ee_idx')],
            },
        ),
    ]
