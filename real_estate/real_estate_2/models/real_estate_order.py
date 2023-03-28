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
    offer_price = fields.Float(string='Best Offer', compute='_compute_offer_price')
    state = fields.Selection(
        [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default=lambda self: _('new'))

    @api.onchange('garden')
    def test_real(self):
        for rec in self:
            if rec.garden:
                rec.garden_orientation = "north"
            if rec.garden:
                rec.garden_area = 10
            else:
                rec.garden_area = 0
                rec.garden_orientation = None

    def action_sold(self):
        for rec in self:
            if "canceled" in rec.state:
                raise UserError("Canceled properties cannot be sold.")

            return self.write({"state": "sold"})

    def action_cancel(self):
        for rec in self:
            if "sold" in rec.state:
                raise UserError("Sold properties cannot be canceled.")

            return self.write({"state": "canceled"})

    from odoo import api
    total = fields.Float(compute='_compute_total')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_offer_price(self):
        for offer in self:
            offer.offer_price = 0
            for rec in range(len(offer.offer_ids)):
                for line in range(rec + 1, len(offer.offer_ids)):
                    if offer.offer_ids[rec].price < offer.offer_ids[line].price:
                        offer.offer_price = offer.offer_ids[line].price
