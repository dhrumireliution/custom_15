# -*- coding: utf-8 -*-


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': '',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_order_views.xml',
        'views/real_estate_properties_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
