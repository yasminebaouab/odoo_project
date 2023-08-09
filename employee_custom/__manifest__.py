{
    'name': "Employee Custom",

    'summary': """
    Employee Custom""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr', 'partner_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/contract.xml',
        'views/employee.xml',
        'views/remuneration_av.xml',
        'views/sol_holiday.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'sequence': -920,
}
