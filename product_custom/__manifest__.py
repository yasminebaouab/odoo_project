# -*- coding: utf-8 -*-
{
    'name': "Product Custom",

    'summary': """
        Product Custom""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/kit.xml',
        'views/category.xml',
        'views/step.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'sequence': -940,
}
