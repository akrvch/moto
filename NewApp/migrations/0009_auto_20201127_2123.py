# Generated by Django 3.1.3 on 2020-11-27 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewApp', '0008_nonloggedcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonloggedcart',
            name='user',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
