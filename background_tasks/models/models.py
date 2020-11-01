# -*- coding: utf-8 -*-

from odoo import api, models, _

class Import(models.TransientModel):
    _name = 'base_import.import'
    _inherit = 'base_import.import'
    _description = 'Base Import'

    @api.model
    def do_legacy(self, id, fields, columns, options, dryrun):
        result = super(Import, self.browse(id)).do(fields, columns, options, dryrun)


    @api.multi
    def do(self, fields, columns, options, dryrun=False):
        cron = self.env['ir.cron'].create({
            'name': "import task",
            'model_id': self.env['ir.model'].search([('model', '=', self._name)], limit=1).id,
            'state': 'code',
            'code': 'model.do_legacy(' + str(self.id) + ',' + str(fields) + ', ' + str(
                columns) + ', ' + str(options) + ', '
                    + str(dryrun) + ')',
            'interval_number': 1,
            'interval_type': 'days',
            'active': True,
            'numbercall': 1
        })

        model_name = self.env[self.res_model]._name

        return "Import task for model {} has been started." \
            .format(model_name)
