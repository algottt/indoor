from webargs import fields
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import validates, ValidationError, pre_load
from marshmallow.validate import Length, Range, OneOf

from app.common.schemas import FilterSchema, SuccessListSchema, sort_one_of
from app.locations.schemas import LocationSchema
from app.devices.utils import check_token
from .models import Device, Contact
from . import constants as DEVICE


class FilterDevicesSchema(FilterSchema):
    sort_by = fields.Str(
        validate=sort_one_of(['id', 'status', 'comment', 'created_at', 'updated_at']),
        missing='created_at'
    )
    query = fields.Str(validate=Length(min=3, max=100), missing=None)
    status = fields.Str(validate=OneOf(choices=dict(DEVICE.STATUSES).values()), missing=None)


class AddContactSchema(ma.Schema):
    name = fields.Str(validate=Length(min=5, max=255), required=True)
    tel = fields.Str(validate=Length(min=10, max=255), required=True)
    comment = fields.Str(validate=Length(max=1024), missing=None)


class ContactSchema(ModelSchema):
    class Meta:
        model = Contact


class DeviceSchema(ModelSchema):
    location = fields.Nested(LocationSchema, many=False)
    contact = fields.Nested(ContactSchema, many=False)

    class Meta:
        model = Device
        exclude = ['uid_token', 'access_token']


class DeviceListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(DeviceSchema()))


class RegisterDeviceSchema(ma.Schema):
    uid_token = fields.Str(validate=Length(min=10, max=255), required=True)

    @validates('uid_token')
    def validate_uid(self, data):  # noqa
        if not check_token(data):
            raise ValidationError('Malformed token')


class RegisteredDeviceSchema(ma.Schema):
    id = fields.Int(validate=Range(min=1), required=True)
    access_token = fields.Str(validate=Length(min=10, max=255), required=True)


class UpdateDeviceSchema(ma.Schema):
    contact_id = fields.Int(validate=Range(min=1), missing=None)
    location_id = fields.Int(validate=Range(min=1), missing=None)
    status = fields.Str(validate=OneOf(choices=dict(DEVICE.STATUSES).values()), missing=None)
    comment = fields.Str(validate=Length(max=255), missing=None)


class UpdateContactSchema(ma.Schema):
    name = fields.Str(validate=Length(min=5, max=255), required=True)
    tel = fields.Str(validate=Length(min=10, max=255), required=True)
    comment = fields.Str(validate=Length(max=1024), missing=None)


class SendCommandSchema(ma.Schema):
    command = fields.Str(validate=OneOf([s[1] for s in DEVICE.COMMANDS]), missing=DEVICE.SHOW_INFO)
    device_ids = fields.List(fields.Int(), validate=Length(min=1), required=True)

    @pre_load
    def check_device_ids(self, data, **_):
        for i in data['device_ids']:
            if not isinstance(i, int):
                raise ValidationError('ValueError: Value must be int', field_name='device_ids')
        return data
