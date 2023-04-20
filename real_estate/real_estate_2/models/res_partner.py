from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('odoo', 'Odoo Mates')])