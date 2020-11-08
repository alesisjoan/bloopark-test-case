# -*- coding: utf-8 -*-
"""
DISCLAIMER: this is for demonstration purposes, take this code by your own responsabilities. This software is not meant
to be updated or upgraded, or to solve issues.
"""
import logging
from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class Import(models.TransientModel):
    _name = 'base_import.import'
    _inherit = 'base_import.import'
    _description = 'Base Import'

    @api.model
    def do_legacy(self, id, fields, columns, options, dryrun):
        # this is the callback of the background task
        return super(Import, self.browse(id)).do(fields, columns, options, dryrun)

    def do(self, fields, columns, options, dryrun=False):
        self.ensure_one()
        model_obj = self.env[self.res_model]
        model_name = model_obj._description or model_obj._name
        # note that we replaced the BaseImport#do statement by the this#do_legacy
        # in code execute, we put python code
        task = self.env['background_tasks.task'].create({
            'name': "Import task",
            'model': self._name,
            'model_name': self._description,
            'extra_info': 'Filename used: {}'.format(self.file_name),
            'code_execute': 'self.env["base_import.import"].do_legacy(' + str(self.id) + ',' +
                            str(fields) + ', ' + str(columns) + ', ' + str(options) + ', '
                            + str(dryrun) + ')',
            'message_chat_start': "Import task for model {} has been started."
                                  " You will be notified by chat when its finished.".format(model_name),
            'message_chat_finish': "Import task for model {} has been finished.".format(model_name),
            'message_systray': ""
        })
        task.systray(task.name)

        return "Import task for model {} has been started." \
               " You will be notified by chat when its finished." \
            .format(model_name)
