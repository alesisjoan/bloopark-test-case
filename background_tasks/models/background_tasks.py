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
        ('closed', 'Closed'),
    ], default='created', readonly=1)

    user_id = fields.Many2one('res.users', readonly=1, string='User',
                              help='The user that triggered the task.')

    model = fields.Char(readonly=1, string='Model Technical Name',
                        help='The model technical name that the task is executed from.')

    model_name = fields.Char(readonly=1, string='Model Name',
                             help='The model that the task is executed from.')

    message_chat_start = fields.Text(readonly=1, string='Message Start',
                                     help='The message that will notify the user when task starts')

    message_chat_finish = fields.Text(readonly=1, string='Message Finish',
                                      help='The message that will notify the user when task finishs')

    message_systray = fields.Char(readonly=1, string='Systray Message',
                                  help='The message located in the systray')

    name = fields.Char(readonly=1)

    code_execute = fields.Text(readonly=1, string='Code to execute',
                               help='The code to be executed')

    extra_info = fields.Text(readonly=1, string='Extra Info', help='Extra info for the task')

    cron_id = fields.Many2one('ir.cron', ondelete='set null', string='Cron',
                              help='The cron that will execute the task')

    exception_message = fields.Text(readonly=1, string='Exception',
                                    help='Result if the task could not be executed.')

    result = fields.Text(readonly=1, string='Result returned', help='The result if any, that the task returned.')

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
        task.systray(task.name)
        return task

    def systray(self, message):
        _logger.debug('module_message_systray {}'
                      .format(self.env['ir.config_parameter'].sudo().get_param('background_tasks.module_message_systray')))
        if self.env['ir.config_parameter'].sudo().get_param('background_tasks.module_message_systray'):
            for task in self:
                current = self.env['systray.user.message'].search([
                    ('user_id', '=', task.user_id.id)
                ]) or self.env['systray.user.message'].create({
                    'user_id': task.user_id.id
                })
                current.message = message

    def notify(self, message):
        for task in self:
            odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
            odoobot = self.env['res.users'].browse(odoobot_id)
            channel_odoo_bot_users = 'Background Tasks: %s' % (task.user_id.name)
            channel_obj = self.env['mail.channel']
            channel_id = channel_obj.search([('name', 'like', channel_odoo_bot_users)]) or \
                         channel_obj.create(
                             {
                                 'name': channel_odoo_bot_users,
                                 'email_send': False,
                                 'channel_type': 'chat',
                                 'public': 'private',
                                 'channel_partner_ids': [(4, odoobot.partner_id.id),
                                                         (4, task.user_id.partner_id.id)]
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
        if self.env['ir.config_parameter'].sudo().get_param('background_tasks.module_send_chat_start'):
            task.notify(task.message_chat_start)
        try:
            _logger.debug("To start task {}".format(task.name))
            task.result = eval(task.code_execute) or ""
            if self.env['ir.config_parameter'].sudo().get_param('background_tasks.module_send_chat_finish'):
                task.notify(task.message_chat_finish)
            task.state = 'executed'
            _logger.debug("Task finished {}".format(task.name))
        except Exception as e:
            _logger.error("Exception for task {}: {}".format(task.name, str(e)))
            task.exception_message = str(e)
            task.state = 'exception'
            if self.env['ir.config_parameter'].sudo().get_param('background_tasks.module_send_chat_finish'):
                task.notify('Task {} Exception has occurred {}'.format(task.name, str(e)))
        finally:
            task.systray('')

    def mark_as_closed(self):
        for s in self:
            s.cron_id = False
            s.state = 'closed'


