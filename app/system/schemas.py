from webargs import fields, validate
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema

from app.common.schemas import FilterSchema, SuccessListSchema
from app.system.models import DeviceHealth


class OSVersionSchema(ma.Schema):
    os_version = fields.Str(validate=validate.Length(min=1, max=1024), required=True)


class SoftwareVersionSchema(ma.Schema):
    software_version = fields.Str(validate=validate.Length(min=1, max=255), missing=None)
    download_url = fields.Str(validate=validate.Length(min=1, max=1024), missing=None)


class FilterDeviceHealthSchema(FilterSchema):
    sort_by = fields.Str(
        validate=validate.OneOf(
            ['device_id', 'software_version', 'created_at']),
        missing='created_at'
    )
    device_id = fields.Str(validate=validate.Length(min=1, max=255), missing=None)
    start_date_time = fields.DateTime(missing=None)
    end_date_time = fields.DateTime(missing=None)


class DeviceHealthSchema(ModelSchema):
    class Meta:
        model = DeviceHealth


class DeviceHealthListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(DeviceHealthSchema()))


class AddDeviceHealthSchema(ma.Schema):
    device_id = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    software_version = fields.Str(validate=validate.Length(min=0, max=255), missing=None)
