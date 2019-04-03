from marshmallow import fields, Schema
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {"invalid": "not a valid image"}

    def _deserialize(self, value, attr, data, **kwargs):

        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class ImageSchema(Schema):
    image = FileStorageField(reuired=True)
