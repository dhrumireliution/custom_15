# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty, float_compare

from odoo.addons.payment import utils as payment_utils


class RealEstateOffers(models.Model):
    _name = "real.estate.offers"
    _description = "Real Estate offers "
    # _inherit = "real_estate.order"
    _order = " price desc"

    price = fields.Float(string='Price')
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner",string="Partner", required=True)
    property_id = fields.Many2one("real_estate.order", required=True)
    # property_type_id = fields.Many2one("real.estate.properties", related="property_id.property_type_id",
    #                                    string="Property Type", store=True)
    # days = fields.Integer(string="Validity (days)", default="7")
    #
    # date_deadline_date = fields.Date(string="Deadline", compute="_compute_date_deadline"
    #                                  , default=fields.datetime.now())
    validity_deadline = fields.Integer(string="Validity(days)", default="7")
    last_date = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
                            , default=fields.datetime.now())
    propertytype = fields.Many2one("real.estate.properties", related='property_id.propertytype')
    company_id = fields.Many2one(related='property_id.company_id', string='Company', store=True, index=True)

    @api.depends("create_date", "validity_deadline")
    def _compute_date_deadline(self):

        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()

            offer.last_date = date + relativedelta(days=offer.validity_deadline)

    def _inverse_date_deadline(self):

        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()

            offer.validity_deadline = (offer.last_date - date).days

    def action_accept(self):
        self.write({"status": "accepted"})
        self.property_id.write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer": self.partner_id})

    def action_refuse(self):
        return self.write({"status": "refused"})

    @api.model
    def write(self, vals):
        # OVERRIDE
        res = super().write(vals)
        self.property_id.state = "offer_received"
        for rec in self:
            if rec.property_id.offer_price and rec.property_id.offer_price > rec.price:
                raise UserError(_("The offer must be higher"))
        return res
