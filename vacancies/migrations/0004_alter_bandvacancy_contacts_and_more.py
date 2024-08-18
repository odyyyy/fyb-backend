# Generated by Django 5.1 on 2024-08-14 19:43

import django.contrib.postgres.fields
import django.db.models.deletion
import vacancies.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_alter_bandvacancy_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='bandvacancy',
            name='contacts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=3, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='bandvacancy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='bandvacancy',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='bandvacancy',
            name='genre',
            field=vacancies.utils.ChoiceArrayField(base_field=models.CharField(max_length=50), choices=[('rock', 'Rock'), ('pop', 'Pop'), ('jazz', 'Jazz'), ('classical', 'Classical'), ('metal', 'Metal'), ('electronic', 'Electronic'), ('other', 'Other')], size=3, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='bandvacancy',
            name='instrument',
            field=models.CharField(choices=[('guitar', 'Guitar'), ('bass', 'Bass'), ('drums', 'Drums'), ('piano', 'Piano'), ('other', 'Other')], max_length=50, verbose_name='Инструмент'),
        ),
        migrations.AlterField(
            model_name='musicianvacancy',
            name='contacts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=3, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='musicianvacancy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='musicianvacancy',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='musicianvacancy',
            name='genre',
            field=vacancies.utils.ChoiceArrayField(base_field=models.CharField(max_length=50), choices=[('rock', 'Rock'), ('pop', 'Pop'), ('jazz', 'Jazz'), ('classical', 'Classical'), ('metal', 'Metal'), ('electronic', 'Electronic'), ('other', 'Other')], size=3, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='musicianvacancy',
            name='instruments',
            field=vacancies.utils.ChoiceArrayField(base_field=models.CharField(max_length=50), choices=[('guitar', 'Guitar'), ('bass', 'Bass'), ('drums', 'Drums'), ('piano', 'Piano'), ('other', 'Other')], size=3, verbose_name='Инструменты'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес мероприятия'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='event_datetime',
            field=models.DateTimeField(verbose_name='Время мероприятия'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='event_type',
            field=models.CharField(max_length=255, verbose_name='Тип мероприятия'),
        ),
        migrations.AlterField(
            model_name='organizervacancy',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
