# Generated by Django 3.0.5 on 2020-04-29 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20200423_0040'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.RemoveField(
            model_name='concert',
            name='eid',
        ),
        migrations.DeleteModel(
            name='Exhibition',
        ),
        migrations.DeleteModel(
            name='held',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Perform',
        ),
        migrations.DeleteModel(
            name='Theater',
        ),
        migrations.DeleteModel(
            name='TicketHas',
        ),
        migrations.DeleteModel(
            name='Time',
        ),
        migrations.RemoveField(
            model_name='ton',
            name='eid',
        ),
        migrations.DeleteModel(
            name='ArtEvents',
        ),
        migrations.DeleteModel(
            name='Concert',
        ),
        migrations.DeleteModel(
            name='TOn',
        ),
    ]
