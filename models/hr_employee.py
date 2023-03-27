from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class EmployeeInherit(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    used_in_driver = fields.Boolean(default=False)
    cargo_ids = fields.One2many('cargo.information', 'driver_id')
