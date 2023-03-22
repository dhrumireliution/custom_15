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

class RealEstateOffers(models.Model):
    _name = "real.estate.offers"
    _description = "Real Estate offers "

    price = fields.Float(string='Price')
    status = fields.Selection(copy=False ,selection=[('accepted', 'Accepted'),('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("real_estate.order", required=True)