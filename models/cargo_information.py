from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CargoInformation(models.Model):
    _name = "cargo.information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cargo Information"
    _rec_name = 'tracking_number'

    creator_id = fields.Many2one('res.users', string="Oluşturan Kişi", readonly=True, required=True,
                                 default=lambda self: self.env.user and self.env.user.id or False)
    operations_officer_id = fields.Many2one('res.partner', required=True, string="Operasyon Yetkilisi")
    responsible_dep_officer_id = fields.Many2one('res.partner', string="Sorumlu Departman Yetkilisi")
    sales_representative_id = fields.Many2one('res.partner', string="Satış Temsilcisi")
    sender_name_id = fields.Many2one('res.partner', required=True, string='Gönderici Adı')
    recipient_name_id = fields.Many2one('hr.contract', required=True, string='Alıcı Adı')
    customer_representative_id = fields.Many2one('res.partner', string="Müşteri Temsilcisi")
    agency_information_id = fields.Many2many('agency.information', string="Acente Bilgileri")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Araç", domain=[('used_in_fleet', '=', False)])
    towing_plate = fields.Char(string="Araç Çeker Plakası", required=True)
    trailer_plate_id = fields.Many2one('trailer', string="Araç Dorse Plakası")
    driver_id = fields.Many2one('hr.employee', string="Şoför Bilgileri", domain=[('used_in_driver', '=', False)])
    trade_type = fields.Selection([
        ('export', 'İhracat'),
        ('import', 'İthalat'),
    ], string="Ticaret Tipi")
    exporting_country_id = fields.Many2one(comodel_name='res.country', string="İhracatçı Ülke", )
    importer_country_id = fields.Many2one(comodel_name='res.country', string="İthalatçı Ülke")
    uploaded_address = fields.Char(string="Yüklenen Adres")
    address_tobe_delivered = fields.Char(string="Teslim Edilecek Adres")
    out_customs_line_id = fields.Many2one('customs', string="Gümrük Çıkış")
    arrival_customs_line_id = fields.Many2one('customs', string="Gümrük Varış")
    start_date = fields.Date(string="İşlemin Başladığı Tarih", default=fields.Date.context_today)
    guess_date = fields.Date(string="Tahmini Varış Yapacağı Tarih")
    finish_date = fields.Date(string="Teslim Edildiği Tarih")
    transit_pass_number = fields.Char(string="Transit Geçiş Belgesi Numarası")
    tracking_number = fields.Char(string='Takip Numarası', required=True,
                                  default=lambda self: self.env['ir.sequence'].next_by_code(
                                      'cargo.information.tracking'))
    cargo_waybill_number = fields.Char(string='Kargo İrsaliye Numarası', required=True,
                                       default=lambda self: self.env['ir.sequence'].next_by_code(
                                           'cargo.information.waybill'))
    product_line_ids = fields.Many2many('product.template', string="Ürünler")
    total_case = fields.Integer(string="Toplam Kap Miktarı", compute="_compute_total_case")
    invoice_line_ids = fields.Many2one('account.move', string="Fatura Bilgileri")
    type_of_transport = fields.Selection(
        [('highway', 'Karayolu'),
         ('seaway', 'Denizyolu'),
         ('airway', 'Havayolu'),
         ('railway', 'Demiryolu'),
         ('forwarder', 'Forwarder')], required=True,
        string="Taşıma Yöntemi")
    explanation = fields.Html(string='Açıklama')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('to_approve', 'Onay Aşamasında'),
        ('approved', 'Onaylandı'),
        ('on_the_way', 'Yolda'),
        ('delivered', 'Teslim Edildi'),
        ('invoiced', 'Faturalandı'),
        ('cancel', 'İptal')], default='draft', string="Status", required=True)
    active = fields.Boolean(string='Aktif', default=True)

    def action_draft(self):
        self.state = 'draft'

    def action_to_approve(self):
        self.state = 'to_approve'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True

    def action_approved(self):
        self.state = 'approved'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True

    def action_on_the_way(self):
        self.state = 'on_the_way'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True

    def action_delivered(self):
        self.state = 'delivered'
        self.vehicle_id.used_in_fleet = False
        self.driver_id.used_in_driver = False

    def action_invoiced(self):
        self.state = 'invoiced'

    def action_cancel(self):
        self.state = 'cancel'
        self.vehicle_id.used_in_fleet = False
        self.driver_id.used_in_driver = False

    @api.onchange('vehicle_id')
    def onchange_vehicle_plate(self):
        self.towing_plate = self.vehicle_id.license_plate

    @api.depends('product_line_ids.case')
    def _compute_total_case(self):
        for rec in self:
            total = sum(rec.product_line_ids.mapped('case'))
            rec.total_case = total
        _logger.info('************************************************************************')


class Trailer(models.Model):
    _name = "trailer"
    _rec_name = "trailer_plate"

    trailer_plate = fields.Char(string="Dorse Plakası")


class CargoSearch(models.Model):
    _name = 'cargo.information.search'

    file = fields.Many2one('cargo.information', string="Dosya")

    def generate_cmr_report(self):
        self.ensure_one()
        [data] = self.read()
        data['emp'] = self.env.context.get('active_ids', [])
        track_number = str(data['file'][1])
        _logger.info('*****************************************************************************')
        _logger.info(str(data))
        _logger.info(str(data['emp']))
        _logger.info(track_number)
        _logger.info(self.env['cargo.information'].browse(data['file']))
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_cmr_report').report_action(
            self.env['cargo.information'].search([('tracking_number', '=', track_number)])
            , data=datas)

    def generate_declaration_report(self):
        self.ensure_one()
        [data] = self.read()
        track_number = str(data['file'][1])
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_declaration_report').report_action(
            self.env['cargo.information'].search([('tracking_number', '=', track_number)]), data=datas)

    def generate_miscellaneous_report(self):
        self.ensure_one()
        [data] = self.read()
        track_number = str(data['file'][1])
        datas = {
            'ids': [],
            'model': 'cargo.information.search',
            'form': data
        }
        return self.env.ref('om_logistic.cargo_miscellaneous_report').report_action(
            self.env['cargo.information'].search([('tracking_number', '=', track_number)]), data=datas)
