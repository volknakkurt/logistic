from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class EmployeeInherit(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    used_in_driver = fields.Boolean(default=False)
    cargo_ids = fields.One2many('cargo.information', 'driver_id')
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'hr.expense'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense._origin.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'hr.expense'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'hr.expense', 'default_res_id': self.id}
        return res