# Generated by Django 3.2.3 on 2021-06-20 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soowa_web', '0006_imageupload_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageUpload',
            new_name='Post',
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='soowa_web.post')),
            ],
        ),
    ]