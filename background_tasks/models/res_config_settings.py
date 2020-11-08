# -*- coding: utf-8 -*-
"""
DISCLAIMER: this is for demonstration purposes, take this code by your own responsabilities.
This software is not meant to be updated or upgraded, or to solve issues.
"""
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_send_chat_start = fields.Boolean('Allow to send chat when task starts')
    module_send_chat_finish = fields.Boolean('Allow to send chat when task finishes')
    module_message_systray = fields.Boolean('Allow to display a systray message when the task is executed')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            module_send_chat_start=self.env['ir.config_parameter'].sudo().get_param(
                'background_tasks.module_send_chat_start'),
            module_send_chat_finish=self.env['ir.config_parameter'].sudo().get_param(
                'background_tasks.module_send_chat_finish'),
            module_message_systray=self.env['ir.config_parameter'].sudo().get_param(
                'background_tasks.module_message_systray')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('background_tasks.module_send_chat_start',
                                                         self.module_send_chat_start)
        self.env['ir.config_parameter'].sudo().set_param('background_tasks.module_send_chat_finish',
                                                         self.module_send_chat_finish)
        self.env['ir.config_parameter'].sudo().set_param('background_tasks.module_message_systray',
                                                         self.module_message_systray)
