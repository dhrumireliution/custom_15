# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstateOfferCreate(models.TransientModel):
    _name = 'estate.offer.create'
    _description = " Estate Offer Create"

    name = fields.Char(string='name', required=False, readonly=False)
