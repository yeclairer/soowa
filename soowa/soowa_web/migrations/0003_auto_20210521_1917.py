# Generated by Django 3.2.3 on 2021-05-21 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soowa_web', '0002_auto_20210521_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gesture',
            name='moveX',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='gesture',
            name='moveY',
            field=models.IntegerField(),
        ),
    ]
