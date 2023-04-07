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


class RealEstateOrders(models.Model):
    _inherit = "real_estate.order"

    def action_sold(self):
        res = super(RealEstateOrders, self).action_sold()
        self.env["account.move"].create(
            {
                "partner_id": self.buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    ({
                        "name": self.name,
                        "quantity": 1.0,
                        "price_unit": self.selling_price * 0.6
                    }),
                    ({
                        "name": "administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.00
                    }),
                ],

            }
        )

        return res
