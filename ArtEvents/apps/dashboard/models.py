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


class Payment(models.Model):
    pid = models.CharField(db_column='Pid', primary_key=True, max_length=20)  # Field name made lowercase.
    address = models.CharField(max_length=200, blank=True, null=True)
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    ticket_num = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payment'


class Perform(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    aid = models.ForeignKey(Artist, models.DO_NOTHING, db_column='Aid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Perform'
        unique_together = (('eid', 'aid'),)


class Subscription(models.Model):
    sid = models.CharField(db_column='Sid', primary_key=True, max_length=100)  # Field name made lowercase.
    email = models.CharField(max_length=100, blank=True, null=True)
    s_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Subscription'


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Buy(models.Model):
    pid = models.OneToOneField(Payment, models.DO_NOTHING, db_column='Pid', primary_key=True)  # Field name made lowercase.
    tid = models.ForeignKey(TicketHas, models.DO_NOTHING, db_column='Tid', related_name='Buy_tid')  # Field name made lowercase.
    eid = models.ForeignKey(TicketHas, models.DO_NOTHING, db_column='Eid', related_name='Buy_eid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'buy'
        unique_together = (('pid', 'tid', 'eid'),)


class DashboardArtist(models.Model):
    aid = models.CharField(db_column='Aid', primary_key=True, max_length=20)  # Field name made lowercase.
    artist_name = models.CharField(max_length=20)
    info = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dashboard_artist'


class DashboardExhibition(models.Model):
    eid = models.CharField(db_column='Eid', primary_key=True, max_length=20)  # Field name made lowercase.
    background = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dashboard_exhibition'


class DashboardHeld(models.Model):
    eid = models.CharField(db_column='Eid', max_length=20)  # Field name made lowercase.
    lid = models.CharField(db_column='Lid', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dashboard_held'


class DashboardLocation(models.Model):
    lid = models.CharField(db_column='Lid', primary_key=True, max_length=20)  # Field name made lowercase.
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dashboard_location'


class DashboardPerform(models.Model):
    eid = models.CharField(db_column='Eid', max_length=20)  # Field name made lowercase.
    aid = models.CharField(db_column='Aid', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dashboard_perform'


class DashboardTheater(models.Model):
    eid = models.CharField(db_column='Eid', primary_key=True, max_length=20)  # Field name made lowercase.
    genre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dashboard_theater'


class DashboardTime(models.Model):
    time_serial = models.CharField(primary_key=True, max_length=20)
    date = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dashboard_time'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Held(models.Model):
    eid = models.OneToOneField(ArtEvents, models.DO_NOTHING, db_column='Eid', primary_key=True)  # Field name made lowercase.
    lid = models.ForeignKey(Location, models.DO_NOTHING, db_column='Lid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'held'
        unique_together = (('eid', 'lid'),)
