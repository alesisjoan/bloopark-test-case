# -*- coding: utf-8 -*-
import logging
from odoo import api, models, fields

_logger = logging.getLogger(__name__)

cron_code_bgt = 'BGT '


class BackgroundTasks(models.Model):
    _name = 'background_tasks.task'
    _description = 'Task to be executed via a cron job'

    state = fields.Selection([
        ('created', 'Created'),
        ('execution', 'In execution'),
        ('executed', 'Executed'),
        ('exception', 'Exception'),
    ], default='created', readonly=1)

    user_id = fields.Many2one('res.users')

    model = fields.Char()

    model_name = fields.Char()

    message_chat_start = fields.Text()

    message_chat_finish = fields.Text()

    message_systray = fields.Char()

    name = fields.Char()

    code_execute = fields.Text()

    cron_id = fields.Many2one('ir.cron', ondelete='set null')

    exception_message = fields.Text()

    result = fields.Text()

    @api.model
    def create(self, vals):
        vals['name'] = vals['name'] + ' ' + self.env['ir.sequence'].next_by_code('background_tasks.task')
        task = super(BackgroundTasks, self).create(vals)
        cron = self.env['ir.cron'].sudo().create({
            'name': cron_code_bgt + task.name,
            'model_id': self.env['ir.model'].search([('model', '=', self._name)], limit=1).id,
            'state': 'code',
            'code': "model.execute({})".format(str(task.id)),
            'interval_number': 1,
            'interval_type': 'days',
            'active': True,
            'numbercall': 1
        })
        task.cron_id = cron.id
        task.user_id = self.env.user.id
        return task

    @api.one
    def systray(self, message):
        # to be implemented
        pass

    @api.one
    def notify(self, message):
        odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
        odoobot = self.env['res.users'].browse(odoobot_id)
        channel_odoo_bot_users = '%s, %s' % (odoobot.name, self.user_id.name)
        channel_obj = self.env['mail.channel']
        channel_id = channel_obj.search([('name', 'like', channel_odoo_bot_users)]) or \
                     channel_obj.create(
                         {
                             'name': channel_odoo_bot_users,
                             'email_send': False,
                             'channel_type': 'chat',
                             'public': 'private',
                             'channel_partner_ids': [(4, odoobot.partner_id.id),
                                                     (4, self.user_id.partner_id.id)]
                         }
                     )

        channel_id.message_post(body=message, author_id=odoobot.id, message_type="comment",
                                subtype="mail.mt_comment")
        return True

    @api.model
    def execute(self, id):
        task = self.browse(id)
        task.state = 'execution'
        self._cr.commit()
        task.notify(task.message_chat_start)
        try:
            _logger.debug("To start task {}".format(task.id))
            task.result = eval(task.code_execute) or ""
            task.notify(task.message_chat_finish)
            task.state = 'executed'
            _logger.debug("Task finished {}".format(task.id))
        except Exception as e:
            _logger.error("Exception for task {}: {}".format(task.name, str(e)))
            task.exception_message = str(e)
            task.state = 'exception'
            task.notify('Exception has occurred {}'.format(str(e)))


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
        return super(Import, self.browse(id)).do(fields, columns, options, dryrun)
        # model_name = self.env[self.browse(id).res_model]._name
        # self.env['background_tasks.chat'].send_message([self.env.user.id],
        #                                                "Import task for model {} has been finished. Result: {}"
        #                                                .format(model_name, result))

    @api.multi
    def do(self, fields, columns, options, dryrun=False):
        model_name = self.env[self.res_model]._name
        self.env['background_tasks.task'].create({
            'name': "Import task",
            'model': self._name,
            'model_name': self._description,
            'code_execute': 'self.env["base_import.import"].do_legacy(' + str(self.id) + ',' + str(
                fields) + ', ' + str(
                columns) + ', ' + str(options) + ', '
                            + str(dryrun) + ')',
            'message_chat_start': "Import task for model {} has been started."
                                  " You will be notified by chat when its finished."
                .format(model_name),
            'message_chat_finish': "Import task for model {} has been finished.".format(model_name),
            'message_systray': "Import {}".format(model_name),
        })

        return "Import task for model {} has been started." \
               " You will be notified by chat when its finished." \
            .format(model_name)
