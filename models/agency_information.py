from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AgencyInformation(models.Model):
    _name = "agency.information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string="Acente Adı")
    address = fields.Char(string="Adres Bilgisi")
    phone = fields.Char(string="Telefon Numarası")
    website = fields.Char(string="Web Sitesi")
    email = fields.Char(string="Email Adresi")
    business_type = fields.Char(string="İşletme Türü")