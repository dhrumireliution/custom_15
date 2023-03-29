# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta

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
    _inherit = "real_estate.order"

    price = fields.Float(string='Price')
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real_estate.order", required=True)
    days = fields.Integer(string="Validity (days)", default="7")
    date_deadline_date = fields.Date(string="Deadline", compute="_compute_date_deadline",
                                     inverse="_inverse_date_deadline", default=fields.datetime.now())

    # @api.depends("days")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.property_id.create_date:
                date = offer.property_id.create_date.date()
                offer.date_deadline_date = date + relativedelta(days=offer.days)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.property_id.create_date:
                date = offer.property_id.create_date.date()
                offer.days = (offer.date_deadline_date - date).days

    def action_accept(self):
        self.write({"status": "accepted"})
        self.property_id.write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer": self.partner_id})

    def action_refuse(self):
        return self.write({"status": "refused"})
