# Generated by Django 2.1.5 on 2020-04-14 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='time',
            field=models.CharField(default='2020-04-06', max_length=20),
            preserve_default=False,
        ),
    ]
