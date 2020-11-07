# -*- coding: utf-8 -*-
import logging
from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class Import(models.TransientModel):
    _name = 'base_import.import'
    _inherit = 'base_import.import'
    _description = 'Base Import'

    @api.model
    def do_legacy(self, id, fields, columns, options, dryrun):
        return super(Import, self.browse(id)).do(fields, columns, options, dryrun)

    def do(self, fields, columns, options, dryrun=False):
        self.ensure_one()
        model_obj = self.env[self.res_model]
        model_name = model_obj._description or model_obj._name
        self.env['background_tasks.task'].create({
            'name': "Import task",
            'model': self._name,
            'model_name': self._description,
            'code_execute': 'self.env["base_import.import"].do_legacy(' + str(self.id) + ',' +
                            str(fields) + ', ' + str(columns) + ', ' + str(options) + ', '
                            + str(dryrun) + ')',
            'message_chat_start': "Import task for model {} has been started."
                                  " You will be notified by chat when its finished.".format(model_name),
            'message_chat_finish': "Import task for model {} has been finished.".format(model_name),
            'message_systray': ""
        })

        return "Import task for model {} has been started." \
               " You will be notified by chat when its finished." \
            .format(model_name)