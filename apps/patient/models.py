from django.db import models

class Guardian(models.Model):
    name = models.CharField(null=False, max_length=32)
    phone = models.CharField(null=False, unique=True, max_length=16)
    relation = models.CharField(null=False, max_length=32)

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'guardians'

class Patients(models.Model):
    name = models.CharField(null=False, max_length=32)
    phone = models.CharField(null=False, unique=True, max_length=16)
    address = models.CharField(null=False, max_length=128)
    id_card = models.CharField(null=False, max_length=64)
    age = models.SmallIntegerField(null=False)
    height = models.SmallIntegerField(null=False)
    weight = models.SmallIntegerField(null=False)
    gender = models.BooleanField(null=False, default=True)
    guardian = models.ForeignKey(Guardian, null=True, on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'patients'




