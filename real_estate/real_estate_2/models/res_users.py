from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("real_estate.order", inverse_name="salesperson",
                                   domain="[('state','=','offer_received')]")
    