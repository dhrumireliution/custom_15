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
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real_estate.order", required=True)
    # validity_date = fields.Integer(string='Validity', default='7')
    # date_deadline = fields.Date(string='Date Deadline', index=True, default=fields.datetime.now(),
    #                             compute='', inverse='')
    validity_days = fields.Integer(string='Validity', default='7')
    # date = fields.Date(string='Date Deadline', default=fields.datetime.now(),
    #                    compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    deadline_date = fields.Date(string='Date Deadline',
                                compute='_compute_date_deadline',inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity_days')
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date:
                line.deadline_date = line.create_date.date() + timedelta(days=line.validity_days)
            else:
                fields.Date.today()
    @api.depends('create_date', 'deadline_date')
    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.validity_days = (rec.deadline_date - rec.create_date.date()).days
            else:
                fields.Date.today()

    def action_accept(self):
        for rec in self:
            if "accepted" in rec.status:
                return self.write({"status": "accepted"})


    def action_refuse(self):
        for rec in self:
            if "refused" in rec.status:
                return self.write({"status": "refused"})

