# -*- coding: utf-8 -*-


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': '',
    'depends': ['sale','mail'],
    'data': [
        'security/ir.model.access.csv',
        'view/real_estate_order_views.xml',
        'view/real_estate_properties_views.xml',
        'view/real_estate_tags_views.xml',
        'view/real_estate_offers.xml',
        'view/res_users.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
