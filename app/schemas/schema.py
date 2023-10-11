from app import ma
from marshmallow import fields

class userSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    email = fields.String()
    password = fields.String()
    perfil = fields.String()
    fecha_creacion = fields.String()
    # fecha_creacion = fields.DateTime()
    
    # objetoNested = fields.Nested(otroSchema, exclude=('id',))
