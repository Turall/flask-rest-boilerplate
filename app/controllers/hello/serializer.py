from marshmallow import fields

from core.extensions import ma


class SampleSerializer(ma.Schema):
    foo = fields.Str()
    bar = fields.Str()
