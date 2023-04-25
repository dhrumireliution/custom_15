# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    propertytype = fields.Many2one("real.estate.properties", string='Property Type', tracking=True)

