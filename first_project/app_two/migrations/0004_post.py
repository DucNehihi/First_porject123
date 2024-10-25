# Generated by Django 5.1.2 on 2024-10-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_two', '0003_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
