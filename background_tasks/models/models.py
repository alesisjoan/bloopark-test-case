# -*- coding: utf-8 -*-

from odoo import api, models, _


class Chat(models.TransientModel):
    _name = 'background_tasks.chat'

    @api.model
    def send_message(self, user_to_ids, message):
        for user_to in user_to_ids:
            user = self.env['res.users'].browse(user_to)
            partner = user.partner_id
            odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
            channel = self.env['mail.channel'].sudo().search([('uuid', '=', user_to)], limit=1) \
                .with_context(mail_create_nosubscribe=True).create({
                'channel_partner_ids': [(4, partner.id), (4, odoobot_id)],
                'public': 'private',
                'channel_type': 'chat',
                'email_send': False,
                'name': 'OdooBot'
            })
            channel.sudo().message_post(body=message, author_id=odoobot_id, message_type="comment",
                                        subtype="mail.mt_comment")
        return True


class Import(models.TransientModel):
    _name = 'base_import.import'
    _inherit = 'base_import.import'
    _description = 'Base Import'

    @api.model
    def do_legacy(self, id, fields, columns, options, dryrun):
        result = super(Import, self.browse(id)).do(fields, columns, options, dryrun)
        model_name = self.env[self.browse(id).res_model]._name
        self.env['background_tasks.chat'].send_message([self.env.user.id],
                                                       "Import task for model {} has been finished. Result: {}"
                                                       .format(model_name, result))

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
        self.env['background_tasks.chat'].send_message([self.env.user.id],
                                                       "Import task for model {} has been started."
                                                       " You will be notified by chat when its finished."
                                                       .format(model_name))

        return "Import task for model {} has been started." \
               " You will be notified by chat when its finished." \
            .format(model_name)
