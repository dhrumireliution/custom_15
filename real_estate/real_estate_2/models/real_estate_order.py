# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils


class RealEstateOrder(models.Model):
    _name = "real_estate.order"
    _inherit = "mail.thread", "mail.activity.mixin"
    _description = "Real Estate Order"

    name = fields.Char(string='Name', required=False, copy=False, readonly=False, default=lambda self: _('New'),
                       tracking=True)
    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=False)
    date_availability = fields.Date(string='Date_availability', copy=False, required=False, index=True)
    expected_price = fields.Float(string='Expected_price', required=False)
    selling_price = fields.Float(string='Selling_price', required=False)
    bedrooms = fields.Integer(string='Bedroom', required=False)
    living_area = fields.Integer(string='Living_area', required=False)
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer(string='Garden_area', required=False)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
    active = fields.Boolean(string='Active', default=True)
    propertytype = fields.Many2one("real.estate.properties", string='Property Type', tracking=True)
    salesperson = fields.Many2one('res.users', string='Salesperson')
    buyer = fields.Many2one('res.partner', string='Buyer')
    tags = fields.Many2many('real.estate.tags', string='Property Tags')
    offer_ids = fields.One2many("real.estate.offers", inverse_name="property_id")
    best_price = fields.Float(string='Best Offer',compute='_compute_best_price' )
    price = fields.Float(string='Price')

    @api.onchange('garden')
    def test_real(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_orientation = "north"
            if rec.garden == True:
                rec.garden_area = 10
            else:
                rec.garden_area = 0
                rec.garden_orientation = None

    from odoo import api
    total = fields.Float(compute='_compute_total')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends('price')
    def _compute_best_price(self):
        for rec in self:
            for i in range(len(rec.offer_ids)):
                for j in range(i + 1, len(rec.offer_ids)):
                    if rec.offer_ids[i].price > rec.offer_ids[j].price:
                        rec.best_price = rec.offer_ids[i].price

#
#
# @api.depends('price')
#     def _compute_offer(self):
#         for rec in self:
#             for line in rec.offer_ids:
#                 if line and line.price > 100000:
#                     rec.offer = line.price
