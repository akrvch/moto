# Generated by Django 3.1.3 on 2020-11-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='motorcycle',
            options={'verbose_name': 'Мотоцикл', 'verbose_name_plural': 'Мотоциклы'},
        ),
        migrations.AlterModelOptions(
            name='mototypes',
            options={'verbose_name': 'Тип мотоцикла', 'verbose_name_plural': 'Типы мотоциклов'},
        ),
        migrations.AlterModelOptions(
            name='motovendor',
            options={'verbose_name': 'Производитель', 'verbose_name_plural': 'Производители'},
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
