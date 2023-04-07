from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CustomsInformation(models.Model):
    _name = "customs"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'customs_name'

    is_abroad = fields.Boolean(string="Yurtdışı Gümrük", default=False)
    area_name = fields.Char(string="Bölge Adı")
    area_code = fields.Char(string="Bölge Kodu")
    customs_name = fields.Char(string="Gümrük Adı")
    customs_code = fields.Char(string="Gümrük Kodu")

