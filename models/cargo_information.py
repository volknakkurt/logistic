from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CargoInformation(models.Model):
    _name = "cargo.information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cargo Information"
    _rec_name = 'tracking_number'

    creator = fields.Many2one('res.users', string="Oluşturan Kişi", readonly=True, required=True,
                              default=lambda self: self.env.user and self.env.user.id or False)
    operations_officer = fields.Many2one('res.partner', required=True, string="Operasyon Yetkilisi")
    responsible_dep_officer = fields.Many2one('res.partner', string="Sorumlu Departman Yetkilisi")
    sales_representative = fields.Many2one('res.partner', string="Satış Temsilcisi")
    sender_name = fields.Many2one('res.partner', required=True, string='Gönderici Adı')
    recipient_name = fields.Many2one('hr.contract', required=True, string='Alıcı Adı')
    customer_representative = fields.Many2one('res.partner', string="Müşteri Temsilcisi")
    agency_information = fields.Many2many('agency.information', string="Acente Bilgileri")
    vehicle = fields.Many2one('fleet.vehicle', string="Araç")
    towing_plate = fields.Char(string="Araç Çeker Plakası", required=True)
    trailer_plate = fields.Many2one('trailer', string="Araç Dorse Plakası")
    driver = fields.Many2one('hr.employee', string="Şoför Bilgileri")
    trade_type = fields.Selection([
        ('export', 'İhracat'),
        ('import', 'İthalat'),
    ], string="Ticaret Tipi")
    exporting_country = fields.Many2one(comodel_name='res.country', string="İhracatçı Ülke",)
    importer_country = fields.Many2one(comodel_name='res.country', string="İthalatçı Ülke")
    uploaded_address = fields.Char(string="Yüklenen Adres")
    address_tobe_delivered = fields.Char(string="Teslim Edilecek Adres")
    out_customs_line_ids = fields.Many2one('customs', string="Gümrük Çıkış")
    arrival_customs_line_ids = fields.Many2one('customs', string="Gümrük Varış")
    start_date = fields.Date(string="İşlemin Başladığı Tarih", default=fields.Date.context_today)
    guess_date = fields.Date(string="Tahmini Varış Yapacağı Tarih")
    finish_date = fields.Date(string="Teslim Edildiği Tarih")
    transit_pass_number = fields.Char(string="Transit Geçiş Belgesi Numarası")
    tracking_number = fields.Char(string='Takip Numarası', required=True,
                                  default=lambda self: self.env['ir.sequence'].next_by_code('cargo.information.tracking'))
    cargo_waybill_number = fields.Char(string='Kargo İrsaliye Numarası', required=True,
                                       default=lambda self: self.env['ir.sequence'].next_by_code('cargo.information.waybill'))
    product_line_ids = fields.Many2many('product.template', string="Ürünler")
    invoice_line_ids = fields.Many2one('account.move', string="Fatura Bilgileri")
    type_of_transport = fields.Selection(
        [('highway', 'Karayolu'),
         ('seaway', 'Denizyolu'),
         ('airway', 'Havayolu'),
         ('railway', 'Demiryolu'),
         ('forwardie', 'Forwardie')], required=True,
        string="Taşıma Yöntemi")
    explanation = fields.Html(string='Açıklama')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('invoiced', 'Faturalandı'),
        ('to_approve', 'Onay Aşamasında'),
        ('approved', 'Onaylandı'),
        ('on_the_way', 'Yolda'),
        ('delivered', 'Teslim Edildi'),
        ('cancel', 'İptal')], default='draft', string="Status", required=True)
    active = fields.Boolean(string='Aktif', default=True)

    @api.onchange('vehicle')
    def onchange_vehicle_plate(self):
        self.towing_plate = self.vehicle.license_plate


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


class OutCustomsInformation(models.Model):
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


class Trailer(models.Model):
    _name = "trailer"
    _rec_name = "trailer_plate"

    trailer_plate = fields.Char(string="Dorse Plakası")


class ProductInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'


class CargoSearch(models.Model):
    _name = 'cargo.information.search'

    file = fields.Many2one('cargo.information', string="Dosya")

    def generate_cmr_report(self):
        self.ensure_one()
        [data] = self.read()
        _logger.info('*****************************************************************************')
        _logger.info(str(data))
        _logger.info(self.env['cargo.information'].browse(data['file']))
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_cmr_report').report_action(self.env['cargo.information'].browse(data['file']), data=datas)

    def generate_declaration_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_declaration_report').report_action(self.env['cargo.information'].browse(data['file']), data=datas)

    def generate_miscellaneous_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_miscellaneous_report').report_action(self.env['cargo.information'].browse(data['file']), data=datas)