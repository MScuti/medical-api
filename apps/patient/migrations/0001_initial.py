# Generated by Django 4.1.3 on 2022-11-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('relation', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'guardians',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('id_card', models.CharField(max_length=64)),
                ('age', models.SmallIntegerField()),
                ('height', models.SmallIntegerField()),
                ('weight', models.SmallIntegerField()),
                ('gender', models.BooleanField(default=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'patients',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]