# Generated by Django 4.2.6 on 2023-10-12 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('horarios', '0001_initial'),
        ('profesores', '0001_initial'),
        ('carreras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ramo',
            name='nrcs',
            field=models.ManyToManyField(blank=True, to='horarios.nrc'),
        ),
        migrations.AddField(
            model_name='ramo',
            name='prerrequisito',
            field=models.ManyToManyField(blank=True, to='carreras.ramo'),
        ),
        migrations.AddField(
            model_name='ramo',
            name='profesores',
            field=models.ManyToManyField(blank=True, to='profesores.profesor'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='ramos',
            field=models.ManyToManyField(to='carreras.ramo'),
        ),
    ]
