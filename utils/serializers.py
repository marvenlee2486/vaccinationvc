from marshmallow import Schema, fields, INCLUDE
from marshmallow.validate import Regexp
from utils.errors import ValidationError


class AuthenticationSerializer(Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=[
            Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", error="Password must be minimum eight characters, at least one uppercase letter and one number"),
        ]
    )

    def dump(self, obj):
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message="Password must be minimum eight characters, at least one uppercase letter and one number")

        return super().dump(obj)