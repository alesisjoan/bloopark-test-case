# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID
from . import models
from . import tests


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].set_param('background_tasks.module_send_chat_start', True)
    env['ir.config_parameter'].set_param('background_tasks.module_send_chat_finish', True)
    env['ir.config_parameter'].set_param('background_tasks.module_message_systray', True)
