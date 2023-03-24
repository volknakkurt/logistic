# -*- coding: utf-8 -*-

{
    'name': 'Logistic Management',
    'version': '1.0.0',
    'category': 'Logistic',
    'author': 'Volkan',
    'sequence': -110,
    'summary': 'Logistic management system',
    'description': "Logistic management system controller",
    'depends': [
        'mail',
        'hr',
        'account',
        'fleet',
        'product',
        'hr_contract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/report_cmr_templates.xml',
        'report/report_declaration_templates.xml',
        'report/report_miscellaneous_templates.xml',
        'views/menu.xml',
        'views/cargo_information_view.xml',
        'views/customs.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}
