# -*- coding: utf-8 -*-





{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'depends': ['sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/real_estate_security.xml',
        'data/data.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'wizard/estate_offer_create_view.xml',
        'wizard/estate_update_offer.xml',
        'view/real_estate_order_views.xml',
        'view/real_estate_properties_views.xml',
        'view/real_estate_tags_views.xml',
        'view/real_estate_offers.xml',
        'view/res_users.xml',
        'view/real_estate_server_action.xml',
        'view/sale_order.xml',
        'report/property_offers.xml',
        'report/report.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}

