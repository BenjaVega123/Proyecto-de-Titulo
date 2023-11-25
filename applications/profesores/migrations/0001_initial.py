# Generated by Django 4.2.6 on 2023-10-12 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('horarios', '0001_initial'),
        ('carreras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(blank=True, max_length=100)),
                ('nombres', models.CharField(blank=True, max_length=50)),
                ('apellidos', models.CharField(blank=True, max_length=50)),
                ('carreras', models.ManyToManyField(blank=True, to='carreras.carrera')),
                ('nrcs', models.ManyToManyField(blank=True, to='horarios.nrc')),
                ('ramos', models.ManyToManyField(blank=True, to='carreras.ramo')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
            },
        ),
    ]
