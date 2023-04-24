# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo import api, fields, models
#
#
# class UsersReport(models.TransientModel):
#     _name = 'users.report'
#
#     price = fields.Float(string='Price')
#     status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
#     partner_id = fields.Many2one("res.partner", string="Partner", required=True)
#
#     def print_xls_report(self, cr, uid, ids, context=None):
#         data = self.read(cr, uid, ids)[0]
#         return {'type': 'ir.actions.report.xml',
#                 'report_name': 'property_users.report_property_users_report.xlsx',
#                 'datas': data
#                 }

    # def print_xls_report(self, cr, uid, ids, context=None, data=None):
    #     rec = self.browse(data)
    #     data = {}
    #     data['form'] = rec.read(['price', 'status', 'partner_id'])
    #     return self.env['report'].get_action(rec, 'property_users.report_property_users_report.xlsx', data=data)


