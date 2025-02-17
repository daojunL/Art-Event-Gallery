# Generated by Django 3.0.4 on 2020-04-23 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.RemoveField(
            model_name='concert',
            name='eid',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.RemoveField(
            model_name='exhibition',
            name='eid',
        ),
        migrations.RemoveField(
            model_name='held',
            name='eid',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.RemoveField(
            model_name='perform',
            name='eid',
        ),
        migrations.RemoveField(
            model_name='theater',
            name='eid',
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
            name='Exhibition',
        ),
        migrations.DeleteModel(
            name='Held',
        ),
        migrations.DeleteModel(
            name='Perform',
        ),
        migrations.DeleteModel(
            name='Theater',
        ),
        migrations.DeleteModel(
            name='TOn',
        ),
    ]
