from app import ma
from marshmallow import fields

class UserBasicSchema(ma.Schema):
    username = fields.String()

    def get_username(self, obj):
        return f'Bienvenido {obj.username}'

class UserAdminSchema(UserBasicSchema):
    id = fields.Integer(dump_only=True)
    password_hash = fields.String()
    saludo_usuario = fields.Method('get_username')

class paisSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()

class provinciasSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    pais = fields.Integer()
    pais_obj = fields.Nested(paisSchema, exclude=('id',))

class localidadesSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    provincia = fields.Integer()
    provincia_obj = fields.Nested(provinciasSchema, exclude=('id',))
