{
    'name': "Declaration Des Bons",
    'summary': "A module for managing declarations of bons.",
    'description': "A module for managing declarations of bons.",
    'author': "Mohamed Ba",
    'sequence': -770,

    'website': "",
    'category': 'Project, Tasks',
    'version': '15.0.1.0.0',
    'depends': ['base',
                'task_work',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/declaration_de_bon.xml',
        'views/declaration_de_bon_controle.xml',
        'views/declaration_de_bon_correction.xml',
        'views/retour_bon_production.xml',
        'views/retour_bon_control.xml',
        'views/retour_bons_correction.xml',
        'views/choix_declaration_bons.xml',
        'views/button.xml',
    ],
    'demo': [],
    'images': [
        'static/description/banner.jpg',
    ],
    'auto_instale': False,
    'application': True,
    'license': 'LGPL-3',
}
