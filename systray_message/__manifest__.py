# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Systray message',
    'version': '13.0',
    'category': '',
    'sequence': 10,
    'author': 'Alesis Manzano',
    'summary': 'Systray message',
    'description': """Puts a systray message for the user. 
            DISCLAIMER: this is for demonstration purposes, take this code by your own responsabilities. This software is not meant to be updated or upgraded, or to 
        solve issues.
    """,
    'website': '',
    'depends': [],
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
