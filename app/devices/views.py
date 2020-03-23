from flask import Blueprint
from sqlalchemy import or_
import logging

from app.locations.models import Location, City
from app.common.decorators import admin_required, auth_required

from lib.factory import db
from lib.utils import success, fail
from lib.webargs import parser


from .models import Device, Contact, ContactException
from .schemas import (
    FilterDevicesSchema,
    UpdateDeviceSchema,
    DeviceSchema,
    DeviceListSchema,
    RegisterDeviceSchema,
    RegisteredDeviceSchema, ContactSchema, AddContactSchema, UpdateContactSchema,)
from .utils import save_device, save_contact

mod = Blueprint('devices', __name__, url_prefix='/devices')


@mod.route('/')
@auth_required
@parser.use_kwargs(FilterDevicesSchema())
def devices_list_view(page, limit, sort_by, query, status):
    """Get list of devices.
    ---
    get:
      tags:
        - Devices
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterDevicesSchema
      responses:
        200:
          content:
            application/json:
              schema: DeviceListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = Device.query

    if status:
        q = q.filter_by(status=status)

    if query:
        q = q.filter(
            or_(
                Device.comment.ilike(f'%{query}%'),
                Device.location.has(Location.address.ilike(f'%{query}%')),
                Device.contact.has(Contact.name.ilike(f'%{query}%')),
                Device.contact.has(Contact.tel.ilike(f'%{query}%')),
                Device.location.has(Location.city.has(City.name.ilike(f'%{query}%')))
            )
        )

    total = q.count()
    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(DeviceListSchema().dump(dict(
        results=q,
        total=total
    )))


@mod.route('/<int:device_id>/')
@auth_required
def device_by_id_view(device_id):
    """Get device by id.
    ---
    get:
      tags:
        - Devices
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: DeviceSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    device = Device.query.get_or_404(device_id)
    return success(DeviceSchema().dump(device))


@mod.route('/', methods=['POST'])
@parser.use_kwargs(RegisterDeviceSchema())
def register_device_view(uid_token):
    """Register new device.
    ---
    post:
      tags:
        - Devices
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: RegisterDeviceSchema
      responses:
        200:
          content:
            application/json:
              schema: RegisteredDeviceSchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    device = save_device(uid_token=uid_token)
    return success(RegisteredDeviceSchema().dump(device))


@mod.route('/<int:device_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdateDeviceSchema())
def update_device_view(device_id, **kwargs):
    """Update device.
    ---
    put:
      tags:
        - Devices
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdateDeviceSchema
      responses:
        200:
          content:
            application/json:
              schema: DeviceSchema
        400:
          content:
            application/json:
              schema: FailSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    device = Device.query.get_or_404(device_id)
    device = save_device(device, **kwargs)
    return success(DeviceSchema().dump(device))


@mod.route('/<int:device_id>/', methods=['DELETE'])
@admin_required
def delete_device_view(device_id):
    """Delete device.
    ---
    delete:
      tags:
        - Devices
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: DeviceSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return success(DeviceSchema().dump(device))


@mod.route('/contacts/<int:contact_id>/', methods=['DELETE'])
@admin_required
def delete_contact_view(contact_id):
    """Delete contact.
    ---
    delete:
      tags:
        - Contacts
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: ContactSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return success(ContactSchema().dump(contact))


@mod.route('/contacts/<int:contact_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdateContactSchema())
def update_contact_view(contact_id, **kwargs):
    """Update contact.
    ---
    put:
      tags:
        - Devices contacts
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdateContactSchema
      responses:
        200:
          content:
            application/json:
              schema: ContactSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    contact = Contact.query.get_or_404(contact_id)
    contact = save_contact(contact, **kwargs)
    return success(ContactSchema().dump(contact))


@mod.route('/contacts/', methods=['POST'])
@admin_required
@parser.use_kwargs(AddContactSchema())
def add_contact_view(**kwargs):
    """Add new contact.
    ---
    post:
      tags:
        - Contacts
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddContactSchema
      responses:
        200:
          content:
            application/json:
              schema: ContactSchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    try:
        contact = save_contact(**kwargs)
    except ContactException as e:
        return fail(str(e))

    return success(ContactSchema().dump(contact))
