from odoo import api, fields, models
from datetime import datetime, timedelta
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
    agency_information_id = fields.Many2one('res.partner', string="Acente Bilgileri")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Araç", domain=[('used_in_fleet', '=', False)])
    towing_plate = fields.Char(string="Araç Çeker Plakası", required=True)
    trailer_plate_id = fields.Many2one('trailer', string="Araç Dorse Plakası", domain=[('used_in_trailer', '=', False)])
    driver_id = fields.Many2one('hr.employee', string="Şoför Bilgileri", domain=[('used_in_driver', '=', False)])
    trade_type = fields.Selection([
        ('export', 'İhracat'),
        ('import', 'İthalat'),
        ('internal', 'Yurtiçi'),
    ], string="Ticaret Tipi")
    exporting_country_id = fields.Many2one(comodel_name='res.country', string="İhracatçı Ülke")
    importer_country_id = fields.Many2one(comodel_name='res.country', string="İthalatçı Ülke")
    uploaded_address = fields.Char(string="Yüklenen Adres")
    address_tobe_delivered = fields.Char(string="Teslim Edilecek Adres")
    out_customs_line_id = fields.Many2one('customs', string="İç Gümrük", domain="[('area_code', '=', customs_area_code)]")
    arrival_customs_line_id = fields.Many2one('customs', string="Dış Gümrük", domain="[('is_abroad', '=', True)]")
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
    customs_area = fields.Selection([
        ('orta_anadolu', 'Orta Anadolu Gümrük ve Ticaret Bölge Müdürlüğü (Ankara)'),
        ('bati_akdeniz', 'Batı Akdeniz Gümrük ve Ticaret Bölge Müdürlüğü (Antalya)'),
        ('uludag', 'Uludağ Gümrük ve Ticaret Bölge Müdürlüğü (Bursa)'),
        ('trakya', 'Trakya Gümrük ve Ticaret Bölge Müdürlüğü (Edirne)'),
        ('gap', 'GAP Anadolu Gümrük ve Ticaret Bölge Müdürlüğü (Gaziantep)'),
        ('dogu_anadolu', 'Doğu Anadolu Gümrük ve Ticaret Bölge Müdürlüğü (Van)'),
        ('ipekyolu', 'İpekyolu Gümrük ve Ticaret Bölge Müdürlüğü (Diyarbakır)'),
        ('dogu_akdeniz', 'Doğu Akdeniz Gümrük ve Ticaret Bölge Müdürlüğü (Hatay / İskenderun)'),
        ('istanbul', 'İstanbul Gümrük ve Ticaret Bölge Müdürlüğü (İstanbul)'),
        ('ege', 'Ege Gümrük ve Ticaret Bölge Müdürlüğü (İzmir)'),
        ('dogu_marmara', 'Doğu Marmara Gümrük ve Ticaret Bölge Müdürlüğü (Kocaeli)'),
        ('firat', 'Fırat Gümrük ve Ticaret Bölge Müdürlüğü (Malatya)'),
        ('orta_akdeniz', 'Orta Akdeniz Gümrük ve Ticaret Bölge Müdürlüğü (Mersin)'),
        ('orta_karadeniz', 'Orta Karadeniz Gümrük ve Ticaret Bölge Müdürlüğü (Samsun)'),
        ('dogu_karadeniz', 'Doğu Karadeniz Gümrük ve Ticaret Bölge Müdürlüğü (Trabzon)'),
        ('bati_marmara', 'Batı Marmara Gümrük ve Ticaret Bölge Müdürlüğü (Tekirdağ)'),
        ('gürbulak', 'Gürbulak Gümrük ve Ticaret Bölge Müdürlüğü (Gürbulak)'),
    ], string="Gümrük Bölgesi")
    customs_area_code = fields.Char(string="Gümrük Bölge Kodu")
    customs_out_code = fields.Char(string="İç Gümrük Kodu", required=True)
    customs_arrival_code = fields.Char(string="Dış Gümrük Kodu", required=True)
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
    product_line_ids = fields.Many2many('product.template', string="Taşınacak Yük")
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
        ('finished', 'Tamamlandı'),
        ('cancel', 'İptal')], default='draft', string="Status", required=True)
    active = fields.Boolean(string='Aktif', default=True)
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')
    payment_method = fields.Selection([
        ('nakit', 'Nakit'),
        ('kredi_karti', 'Kredi Kartı'),
        ('banka_transferi', 'Banka Transferi'),
        ('cek', 'Çek'),
        ('diger', 'Diğer')
    ], string="Ödeme Şekli")
    payment_time = fields.Date(string="Ödeme Zamanı")
    freight_cost = fields.Float(string="Navlun Ücreti")
    is_it_paid = fields.Boolean(string="Ödeme Durumu", compute="_compute_is_it_paid")
    warning_message = fields.Char(string="Ödeme Bilgisi", compute='_compute_warning_message')

    @api.depends('payment_time', 'state')
    def _compute_is_it_paid(self):
        for record in self:
            if record.payment_time and record.state != 'finished':
                today = datetime.today().date()
                if record.payment_time and (record.payment_time - today <= timedelta(days=5)):
                    record.is_it_paid = True
                else:
                    record.is_it_paid = False
            else:
                record.is_it_paid = False

    def _compute_warning_message(self):
        for record in self:
            if record.is_it_paid:
                record.warning_message = "Ödeme Bekleyen"
            elif record.state == 'finished':
                record.warning_message = "Ödemesi Alındı"
            else:
                record.warning_message = ""

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'cargo.information'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense._origin.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'cargo.information'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'cargo.information', 'default_res_id': self.id}
        return res

    def action_draft(self):
        self.state = 'draft'

    def action_to_approve(self):
        self.state = 'to_approve'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True
        self.trailer_plate_id.used_in_trailer = True

    def action_approved(self):
        self.state = 'approved'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True
        self.trailer_plate_id.used_in_trailer = True

    def action_on_the_way(self):
        self.state = 'on_the_way'
        self.vehicle_id.used_in_fleet = True
        self.driver_id.used_in_driver = True
        self.trailer_plate_id.used_in_trailer = True

    def action_delivered(self):
        self.state = 'delivered'
        self.vehicle_id.used_in_fleet = False
        self.driver_id.used_in_driver = False
        self.trailer_plate_id.used_in_trailer = False

    def action_invoiced(self):
        self.state = 'invoiced'

    def action_finished(self):
        self.state = 'finished'

    def action_cancel(self):
        self.state = 'cancel'
        self.vehicle_id.used_in_fleet = False
        self.driver_id.used_in_driver = False
        self.trailer_plate_id.used_in_trailer = False

    @api.onchange('customs_area', 'trade_type')
    def onchange_customs_area(self):
        if self.trade_type == 'export':
            if self.customs_area == 'orta_anadolu':
                self.customs_area_code = '060000'
            elif self.customs_area == 'bati_akdeniz':
                self.customs_area_code = '070000'
            elif self.customs_area == 'uludag':
                self.customs_area_code = '160000'
            elif self.customs_area == 'trakya':
                self.customs_area_code = '220000'
            elif self.customs_area == 'gap':
                self.customs_area_code = '270000'
            elif self.customs_area == 'dogu_anadolu':
                self.customs_area_code = '650000'
            elif self.customs_area == 'ipekyolu':
                self.customs_area_code = '210000'
            elif self.customs_area == 'dogu_akdeniz':
                self.customs_area_code = '310000'
            elif self.customs_area == 'istanbul':
                self.customs_area_code = '340000'
            elif self.customs_area == 'ege':
                self.customs_area_code = '350000'
            elif self.customs_area == 'dogu_marmara':
                self.customs_area_code = '410000'
            elif self.customs_area == 'firat':
                self.customs_area_code = '440000'
            elif self.customs_area == 'orta_akdeniz':
                self.customs_area_code = '330000'
            elif self.customs_area == 'orta_karadeniz':
                self.customs_area_code = '550000'
            elif self.customs_area == 'dogu_karadeniz':
                self.customs_area_code = '610000'
            elif self.customs_area == 'bati_marmara':
                self.customs_area_code = '590000'
            elif self.customs_area == 'gürbulak':
                self.customs_area_code = '040001'
            else:
                self.customs_area_code = ''
        elif self.trade_type == 'import':
            if self.customs_area == 'orta_anadolu':
                self.customs_area_code = '060000'
            elif self.customs_area == 'bati_akdeniz':
                self.customs_area_code = '070000'
            elif self.customs_area == 'uludag':
                self.customs_area_code = '160000'
            elif self.customs_area == 'trakya':
                self.customs_area_code = '220000'
            elif self.customs_area == 'gap':
                self.customs_area_code = '270000'
            elif self.customs_area == 'dogu_anadolu':
                self.customs_area_code = '650000'
            elif self.customs_area == 'ipekyolu':
                self.customs_area_code = '210000'
            elif self.customs_area == 'dogu_akdeniz':
                self.customs_area_code = '310000'
            elif self.customs_area == 'istanbul':
                self.customs_area_code = '340000'
            elif self.customs_area == 'ege':
                self.customs_area_code = '350000'
            elif self.customs_area == 'dogu_marmara':
                self.customs_area_code = '410000'
            elif self.customs_area == 'firat':
                self.customs_area_code = '440000'
            elif self.customs_area == 'orta_akdeniz':
                self.customs_area_code = '330000'
            elif self.customs_area == 'dogu_karadeniz':
                self.customs_area_code = '550000'
            elif self.customs_area == 'bati_marmara':
                self.customs_area_code = '590000'
            elif self.customs_area == 'gürbulak':
                self.customs_area_code = '040001'
            else:
                self.customs_area_code = ''
        else:
            self.customs_area_code = ''

    @api.onchange('out_customs_line_id')
    def onchange_out_customs_line_id(self):
        self.customs_out_code = self.out_customs_line_id.customs_code

    @api.onchange('arrival_customs_line_id')
    def onchange_arrival_customs_line_id(self):
        self.customs_arrival_code = self.arrival_customs_line_id.customs_code


    @api.onchange('vehicle_id')
    def onchange_vehicle_plate(self):
        self.towing_plate = self.vehicle_id.license_plate

    @api.depends('product_line_ids.case')
    def _compute_total_case(self):
        for rec in self:
            total = sum(rec.product_line_ids.mapped('case'))
            rec.total_case = total
        _logger.info('************************************************************************')


class CargoSearch(models.Model):
    _name = 'cargo.information.search'

    file = fields.Many2one('cargo.information', string="Dosya")

    def generate_cmr_report(self):
        self.ensure_one()
        [data] = self.read()
        data['emp'] = self.env.context.get('active_ids', [])
        track_number = str(data['file'][1])
        _logger.info('*****************************************************************************')
        _logger.info(self.env['cargo.information'].search([('tracking_number', '=', track_number)]))
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
