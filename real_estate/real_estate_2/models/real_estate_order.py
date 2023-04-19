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
    _order = " propertytype desc"

    name = fields.Char(string='Title', required=False, readonly=False, default=lambda self: _('New'),
                       tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            index=True, default=lambda self: _('New'))

    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=False)
    date_availability = fields.Date(string='Date_availability', copy=False, required=False, index=True)
    expected_price = fields.Float(string='Expected_price', required=False)
    selling_price = fields.Float(string='Selling_price', required=False, readonly=True)
    bedrooms = fields.Integer(string='Bedroom', required=False)
    living_area = fields.Integer(string='Living_area(sqm)', required=False)
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer(string='Garden_area', required=False)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
    active = fields.Boolean(string='Active', default=True)
    propertytype = fields.Many2one("real.estate.properties", string='Property Type', tracking=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tags = fields.Many2many('real.estate.tags', string='Property Tags')
    offer_ids = fields.One2many("real.estate.offers", inverse_name="property_id")
    offer_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default=lambda self: _('new'), string='Status',
        tracking=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True)
    cancellation_date = fields.Date(string='Cancellation Date ', copy=False, required=False, index=True)
    email = fields.Char(string='Emails')

    # _sql_constraints = [("check_expected_price", "CHECK(expected_price > 0)",
    #                      "A property expected price must be strictly positive"),
    #                     ("check_selling_price", "CHECK(selling_price >= 0)",
    #                      "A property selling price must be positive"),
    #                     ("check_offer_price", "CHECK(offer_price >= 0)",
    #                      "An offer price must be strictly positive")]

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

    # @api.onchange('offer_ids')
    # def offer_ids(self):
    #     for rec in self:
    #         if rec.offer_ids:
    #             self.write({"status": "offer_received"})

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

    total = fields.Float(compute='_compute_total')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.offer_price = max(rec.offer_ids.mapped("price"))

    @api.constrains('expected_price')
    def check_expected_price(self):
        for quant in self:
            if quant.expected_price and quant.expected_price <= 0:
                raise ValidationError(
                    _("A property expected price must be strictly positive"
                      ))

    @api.constrains('selling_price')
    def check_selling_price(self):
        for quant in self:
            if quant.selling_price and quant.selling_price <= 0:
                raise ValidationError(
                    _("A property selling price must be positive"
                      ))

    @api.constrains('offer_price')
    def check_offer_price(self):
        for quant in self:
            if quant.offer_price and quant.offer_price <= 0:
                raise ValidationError(
                    _("An offer price must be strictly positive"
                      ))

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for quant in self:
            if quant.selling_price and quant.selling_price <= quant.expected_price * 0.9:
                raise ValidationError(
                    _(" the selling price cannot be lower than 90% of the expected price"
                      ))

    @api.ondelete(at_uninstall=False)
    def _unlink_only_if_open(self):
        for statement in self:
            if statement.state not in ['new', 'canceled']:
                raise UserError(
                    _("Only new and canceled properties can be deleted."))

    # @api.onchange('offer_ids')
    # def offer(self):
    #     for rec in self:
    #         if rec.offer_ids:
    #             rec.write({"state": "offer_received"})
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('real_estate.order' or _('New'))
        res = super(RealEstateOrder, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        defaults = super(RealEstateOrder, self).default_get(fields)
        defaults['cancellation_date'] = datetime.now() + timedelta(days=5)
        return defaults

    @api.model
    def update_state_cancel(self):
        expired_contracts = self.search(
            [('state', 'not in', ['offer_received', 'canceled', 'offer_accepted', 'sold']),
             ('cancellation_date', '=', fields.Date.today())])
        expired_contracts.write({'state': 'canceled'})

    def name_get(self):
        if self._context.get('real_estate_show_buyer_name'):
            res = []
            for order in self:
                name = order.name
                if order.buyer.name:
                    name = '%s - %s' % (name, order.buyer.name)
                res.append((order.id, name))
            return res
        return super(RealEstateOrder, self).name_get()

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if self._context.get('sale_show_partner_name'):
            if operator == 'ilike' and not (name or '').strip():
                domain = []
            elif operator in ('ilike', 'like', '=', '=like', '=ilike'):
                domain = expression.AND([
                    args or [],
                    ['|', ('name', operator, name), ('buyer.name', operator, name)]
                ])
                return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
        return super(RealEstateOrder, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                         name_get_uid=name_get_uid)

    @staticmethod
    def action_real_estate():
        print("Button Is Clicked")
        return {
            'name': 'Server Action',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'domain': [],
            'res_model': 'real_estate.order',
            'target': 'current'
        }

    def action_send_mail(self):
        templet = self.env.ref('real_estate_2.email_template_properties_offers')
        for rec in self:
            templet.send_mail(rec.id)
