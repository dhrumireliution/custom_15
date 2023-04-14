{
    'name': 'Real Estate Account',
    'version': '1.0',
    'category': '',
    'depends': ['real_estate_2', 'account', 'mail'],
    'data': [
            'security/ir.model.access.csv',
            'report/estate_report_templet.xml',
         ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
