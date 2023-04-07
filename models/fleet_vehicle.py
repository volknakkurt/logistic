from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class VehicleInherit(models.Model):
    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'

    used_in_fleet = fields.Boolean(default=False)
    cargo_ids = fields.One2many('cargo.information', 'vehicle_id')
    visa_expiry_date = fields.Date(string="Vize Bitiş Tarihi")
    insurance_expiry_date = fields.Date(string="Sigorta Bitiş Tarihi")
    is_expired_soon = fields.Boolean(string="Vize/Sigorta Tarihi Yaklaşmış", compute="_compute_is_expired_soon")
    warning_message = fields.Char(string="Uyarı Mesajı", compute='_compute_warning_message')

    @api.depends('visa_expiry_date', 'insurance_expiry_date')
    def _compute_is_expired_soon(self):
        for record in self:
            if record.visa_expiry_date or record.insurance_expiry_date:
                today = datetime.today().date()
                if record.visa_expiry_date and (record.visa_expiry_date - today <= timedelta(days=30)):
                    record.is_expired_soon = True
                elif record.insurance_expiry_date and (record.insurance_expiry_date - today <= timedelta(days=30)):
                    record.is_expired_soon = True
                else:
                    record.is_expired_soon = False
            else:
                record.is_expired_soon = False

    def _compute_warning_message(self):
        for record in self:
            if record.is_expired_soon:
                record.warning_message = "Vize/Sigorta yaklaşıyor!"
            else:
                record.warning_message = ""
