from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class VehicleInherit(models.Model):
    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'

    used_in_fleet = fields.Boolean(default=False)
    cargo_ids = fields.One2many('cargo.information', 'vehicle_id')
    is_rented = fields.Boolean(strng="Kiralık")
