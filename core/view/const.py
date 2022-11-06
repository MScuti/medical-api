from django.db import models

# Serializer filed attr
INT = dict(null=False)
FLOAT = dict(null=False)
STR = dict(null=False, blank=True, max_length=512)
TEXT = dict(null=False, blank=True, max_length=65535)
DATETIME = dict(null=False, format="%Y-%m-%d %H:%M:%S")


MODEL_FIELD_MAP = dict(
    int=dict(field=models.IntegerField, options=INT),
    str=dict(field=models.CharField, options=STR),
    text=dict(field=models.CharField, options=TEXT),
    float=dict(field=models.FloatField, options=FLOAT),
    datetime=dict(field=models.DateTimeField, options=DATETIME),
)