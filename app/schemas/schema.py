from app import ma
from marshmallow import fields

class UserBasicSchema(ma.Schema):
    username = fields.String()

class UserAdminSchema(UserBasicSchema):
    id = fields.Integer(dump_only=True)
    password_hash = fields.String()
