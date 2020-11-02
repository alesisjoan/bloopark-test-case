# -*- coding: utf-8 -*-
{
    'name': "background_tasks",

    'summary': """
        Runs a (heavy) task in background and notify user when it's finished""",

    'description': """
        The purpose is to run a heavy task, yielding a message to the user that the task has began so he can do other things while the task is being executed.
        Finally, it sends a message to the user that the task finished. This avoid the timeout for suchs task like a heavy picking (eg more than 500 elements).
    """,

    'author': "Alesis Manzano",
    'website': "http://alesisjoan.github.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}