# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BouquetRequest(models.Model):
    bouquet_request_id = models.AutoField(primary_key=True)
    bouquet = models.ForeignKey('BouquetType', models.DO_NOTHING)
    request = models.ForeignKey('ServiceRequest', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bouquet_request'


class BouquetType(models.Model):
    bouquet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'bouquet_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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
    id = models.BigAutoField(primary_key=True)
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


class ServiceRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey('Users', models.DO_NOTHING)
    packer = models.ForeignKey('Users', models.DO_NOTHING, related_name='servicerequest_packer_set', blank=True, null=True)
    courier = models.ForeignKey('Users', models.DO_NOTHING, related_name='servicerequest_courier_set', blank=True, null=True)
    client_name = models.CharField(max_length=30, blank=True, null=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    client_address = models.CharField(max_length=100, blank=True, null=True)
    receiving_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'service_request'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    login = models.CharField(max_length=15)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'
