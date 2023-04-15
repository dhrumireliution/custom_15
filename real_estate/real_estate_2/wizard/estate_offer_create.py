# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstateOfferCreate(models.TransientModel):
    _name = 'estate.offer.create'
    _description = " Estate Offer Create"

    name = fields.Char(string='Name', required=False)
    propertytype = fields.Many2one("real.estate.properties", string='Property Type', tracking=True)

    @staticmethod
    def action_create_offers(self):
        print("Button Is Clicked")
        vals = {
            'propertytype': self.propertytype.id,
            'name': self.name,
            'company_id': self.env.company.id

        }
        self.env['real_estate.order'].create(vals)
