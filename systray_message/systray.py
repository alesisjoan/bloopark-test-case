from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class UserMessage(models.Model):
    _name = 'systray.user.message'

    message = fields.Char()
    user_id = fields.Many2one('res.users')

    @api.model
    def update(self, message):
        user_message = self.env['systray.user.message'].search([
            ('user_id', '=', self.env.user.id)
        ], limit=1)
        if user_message:
            user_message.message = message
        else:
            self.env['systray.user.message'].create({
                'user_id': self.env.user.id,
                'message': message,
            })


class SystrayBadge(models.TransientModel):
    _name = "systray.badge"
    _description = "Puts a custom message in the systray"

    @api.model
    def get_message(self):
        message_user = self.env['systray.user.message'].search([
            ('user_id', '=', self.env.user.id)
        ], limit=1)
        try:
            return message_user.message or ''
        except Exception as e:
            return ''
