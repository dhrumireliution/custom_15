# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstateUpdateOffer(models.TransientModel):
    _name = 'estate.update.offer'
    _description = " Estate Update Offer"

    # offer_ids = fields.One2many("real_estate.order", inverse_name="property_id")
    # offer_ids = fields.One2many("real.estate.offers", inverse_name="property_id")
    offer_id = fields.Many2one('real_estate.order')
    date_availability = fields.Date(string='Date_availability', copy=False, required=False, index=True)
    expected_price = fields.Float(string='Expected_price', required=False)
    selling_price = fields.Float(string='Selling_price', required=False, readonly=True)
    bedrooms = fields.Integer(string='Bedroom', required=False)

    def action_update_offers(self):
       pass