from odoo import models , fields  , api
from odoo.exceptions import ValidationError
from datetime import date

class HmsCustomerInherit(models.Model):
    _name = 'res.partner'
    _inherit='res.partner'

    customer1 = fields.Char()

