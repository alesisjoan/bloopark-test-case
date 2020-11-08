# coding: utf-8
from odoo.tests import common

class TestBackgrounTask(common.TransactionCase):

    def test_create(self):
        task = self.env['background_tasks.task'].create({
            'name': "Import task",
            'model': 'base_import.import',
            'model_name': 'base_import.import',
            'extra_info': 'Filename used: stock.product.lot.csv',
            'code_execute': 'print("Hello world")',
            'message_chat_start': "Message start chat",
            'message_chat_finish': "Message finish chat",
            'message_systray': "Message systray"
        })
        self.assertTrue(task.cron_id)
        self.assertTrue(task.cron_id.id > 0)
        self.assertTrue(task.cron_id.active)
        self.assertTrue(task.user_id)
        self.assertTrue(task.user_id.id > 0)

