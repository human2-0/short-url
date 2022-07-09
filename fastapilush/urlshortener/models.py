from tortoise import fields
from tortoise.models import Model


class TortoiseUrl(Model):
    id = fields.IntField(pk=True, generated=True)
    longurl = fields.CharField(min_length=10, max_length=255, unique=True)
    path = fields.CharField(max_length=255,null=True, unique=True)
    shorturl = fields.TextField(null=True)

    class Meta:
        table = "url"
