# Generated by Django 3.2.3 on 2021-06-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soowa_web', '0004_gesture_gesturenum'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]