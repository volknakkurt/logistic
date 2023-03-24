# -*- coding:utf-8 -*-

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class CargoCMRReport(models.AbstractModel):
    _name = 'report.om_logistic.report_cmr_templates'
    _description = 'CMR Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.info('********************* TEST *************************')
        model = 'cargo.information.search'
        docs = self.env[model].browse(self.env.context.get('active_ids', []))
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }
