# -*- coding: utf-8 -*-
{
    'name': "Merge Invoices to assign",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Assign Employees
    """,

    'sequence': -300,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr'],

    # always loaded
    'data': [
        # "'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},

}
