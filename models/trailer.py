from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class Trailer(models.Model):
    _name = "trailer"
    _rec_name = "trailer_plate"

    used_in_trailer = fields.Boolean(default=False)
    cargo_ids = fields.One2many('cargo.information', 'trailer_plate_id')
    trailer_plate = fields.Char(string="Dorse Plakası")
    dorse_turu = fields.Selection([
        ('kapali_dorse', 'Kapalı Dorse'),
        ('tir_dorsesi', 'Tır Dorsesi'),
        ('platform_dorse', 'Platform Dorse'),
        ('frigorifik_dorse', 'Frigorifik Dorse'),
        ('damperli_dorse', 'Damperli Dorse'),
        ('tanker_dorse', 'Tanker Dorse'),
        ('konteyner_dorse', 'Konteyner Dorse'),
        ('cekici_dorse', 'Çekici Dorse')
    ], string='Dorse Türü')
    dorse_alt_kategori = fields.Selection([
        ('acik', 'Açık'),
        ('kapali', 'Kapalı'),
        ('yari_acik', 'Yarı Açık'),
        ('sal', 'Sal Dorse'),
        ('tenteli', 'Tenteli Dorse'),
        ('lowbed', 'Lowbed Dorse'),
        ('kilcik', 'Kılçık Dorse'),
        ('midilli', 'Midilli Dorse'),
        ('pilot', 'Pilot Dorse'),
        ('liftmaster', 'Liftmaster Dorse'),
    ], string='Dorse Alt Kategori')
    capacity = fields.Float(string='Taşıma Kapasitesi(Kap)')
    volume = fields.Float(string='Hacim', compute='_compute_volume', store=True, readonly=True)
    length = fields.Float(string='Uzunluk')
    width = fields.Float(string='Genişlik')
    height = fields.Float(string='Yükseklik')

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.length * rec.width * rec.height

