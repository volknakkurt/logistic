# -*- coding:utf-8 -*-

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class CargoMiscellaneousReport(models.AbstractModel):
    _name = 'report.om_logistic.report_miscellaneous_templates'
    _description = 'Miscellaneous Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.info('********************* TEST *************************')
        model = 'cargo.information'
        cargo_id = data['file'][1]
        _logger.info(data['file'][1])
        _logger.info(data['file'][0])

        docs = self.env[model].browse(cargo_id)
        _logger.info(str(docs))
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }
