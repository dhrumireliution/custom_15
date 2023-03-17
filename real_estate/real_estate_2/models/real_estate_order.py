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
    _description = "Real Estate Order"

    name = fields.Char(string='Name', required=True, copy=False, readonly=False, default=lambda self: _('New'))
    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=True)
    date_availability = fields.Date(string='Date_availability', copy=False, required=True, index=True)
    expected_price = fields.Float(string='Expected_price', required=True)
    selling_price = fields.Float(string='Selling_price', required=True)
    bedrooms = fields.Integer(string='Bedroom', required=True)
    living_area = fields.Integer(string='Living_area', required=True)
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer(string='Garden_area', required=True)
    garden_orientation = fields.Selection([('north', 'North'),('south', 'South'),('west', 'West'),('east','East')])
    active = fields.Boolean(string='Active')