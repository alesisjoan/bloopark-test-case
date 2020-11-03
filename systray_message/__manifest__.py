# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Systray message',
    'version': '12.0',
    'category': '',
    'sequence': 10,
    'author': 'Alesis Manzano',
    'summary': 'Systray message',
    'description': "Puts a systray message for the user",
    'website': '',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/badge.xml',
    ],
}
