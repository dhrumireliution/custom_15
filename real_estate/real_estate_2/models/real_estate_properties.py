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


class RealEstateProperties(models.Model):
    _name = "real.estate.properties"
    _description = "Real Estate Order"
    _order = " name desc"

    name = fields.Char(string='Name', required=False)
    property_ids = fields.One2many("real_estate.order", inverse_name="propertytype", string='properties' )
    sequence = fields.Integer('Sequence', default=1)
    # expected_price = fields.Float(string='Expected_price', required=False)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default=lambda self: _('new'))

    _sql_constraints = [
        ('unique_property_type_name', 'unique (name)', 'property type must be unique.')
    ]



