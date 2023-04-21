# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstateUpdateOffer(models.TransientModel):
    _name = 'estate.update.offer'
    _description = " Estate Update Offer"

    tags = fields.Many2many('real.estate.tags', string='Property Tags')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)

    def action_update_offers(self):
        active_id = self._context.get('active_id')
        upd_var = self.env['real_estate.order'].browse(active_id)
        tag_lst = []
        for vals in self.tags:
            tag_lst.append(vals.id)
        # lst2 = []
        # for vals2 in self.offer_ids:
        #     lst2.append((0,0,{
        #         'price': vals2.price,
        #         'partner_id': vals2.partner_id.id,
        #         'status': vals2.status,
        #         'validity': vals2.validity,
        #         'date_deadline': vals2.date_deadline,
        #         'property_id': vals2.property_id
        #     }))
        vals = {
            'buyer': self.buyer.id,
            'tags': [(6, 0, tag_lst)],
            # 'offer_ids': lst2
        }
        upd_var.update(vals)