from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ProductInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    case = fields.Integer(string="Kap Miktarı")