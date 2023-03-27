from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CustomsInformation(models.Model):
    _name = "customs"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "reference"

    reference = fields.Char(string="Referans")
    customs_name = fields.Char(string="Gümrük Adı")
    customs_code = fields.Char(string="Gümrük Kodu")
    exit_gate = fields.Selection([
        ('kapikule', 'Kapıkule Gümrük Kapısı'),
        ('hamzabeyli', 'Hamzabeyli Gümrük Kapısı'),
        ('ipsala', 'İpsala Gümrük Kapısı'),
        ('pazarkule', 'Pazarkule Gümrük Kapısı'),
        ('derekoy', 'Dereköy Gümrük Kapısı'),
        ('sarp', 'Sarp Gümrük Kapısı'),
        ('cilvegozlu', 'Cilvegözlü Gümrük Kapısı'),
        ('habur', 'Habur Gümrük Kapısı'),
        ('gürbulak', 'Gürbulak Gümrük Kapısı'),
        ('esendere', 'Esendere Gümrük Kapısı'),
        ('kapikoy', 'Kapıköy Gümrük Kapısı'),
        ('turkgozu', 'Türkgözü Gümrük Kapısı'),
        ('sarpi', 'Sarpi Gümrük Kapısı')
    ], string="Gümrük Kapısı")
