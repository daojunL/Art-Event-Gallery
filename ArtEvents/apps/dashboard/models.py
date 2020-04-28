# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ArtEvents(models.Model):
    eid = models.CharField(db_column='Eid', primary_key=True, max_length=60)  # Field name made lowercase.
    title = models.CharField(max_length=60, blank=True, null=True)
    e_image = models.CharField(max_length=200, blank=True, null=True)
    seatmap = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Art_Events'


class Artist(models.Model):
    aid = models.CharField(db_column='Aid', primary_key=True, max_length=20)  # Field name made lowercase.
    artist_name = models.CharField(max_length=40, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Artist'


class Concert(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    concert_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Concert'


class Exhibition(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    background = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Exhibition'


class Location(models.Model):
    lid = models.CharField(db_column='Lid', primary_key=True, max_length=20)  # Field name made lowercase.
    longitude = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Location'


class Perform(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    aid = models.ForeignKey(Artist, models.DO_NOTHING, db_column='Aid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Perform'
        unique_together = (('eid', 'aid'),)


class TOn(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    time_serial = models.ForeignKey('Time', models.DO_NOTHING, db_column='time_serial')

    class Meta:
        managed = False
        db_table = 'T_on'
        unique_together = (('eid', 'time_serial'),)


class Theater(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    genre = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Theater'


class TicketHas(models.Model):
    tid = models.CharField(db_column='Tid', primary_key=True, max_length=20)  # Field name made lowercase.
    eid = models.ForeignKey(ArtEvents, models.DO_NOTHING, db_column='Eid')  # Field name made lowercase.
    price = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    refund_policy = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ticket_has'
        unique_together = (('tid', 'eid'),)


class Time(models.Model):
    time_serial = models.CharField(primary_key=True, max_length=20)
    date_ymd = models.CharField(db_column='date_YMD', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Time'


class Held(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    lid = models.ForeignKey(Location, models.DO_NOTHING, db_column='Lid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'held'
        unique_together = (('eid', 'lid'),)
