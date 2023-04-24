from  odoo import models, fields,api
from  odoo.exceptions import ValidationError
from  datetime import date
import re

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()

    age = fields.Integer(compute='calc_age', store=True)
    CR_Ratio = fields.Float()
    pcr = fields.Boolean()
    image = fields.Binary()
    blood = fields.Selection([('AB', 'AB'), ('A-', 'A+')], default="AB")
    states = fields.Selection([('undetermined', 'undetermined'), ('good', 'good')], default="good")
    address = fields.Text()
    history = fields.Html()
    email = fields.Text()

                      # relations

    department = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department.capacity')
    doctors = fields.Many2many("hms.doctor")
    level_logs = fields.One2many('hms.patient.log', 'patients')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'this email already exits')
    ]

    @api.constrains('age')
    def check_age(self):
        if self.age < 0:
            raise ValidationError('age cant be equal zero or  smaller than zero')

    @api.depends('birth_date')
    def calc_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) <
                    (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.onchange('birth_date')
    def change_pcr(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    # 'title': ('pcr changed'),
                    'message': 'PCR has been changed '
                }
            }

    @api.onchange('states')
    def create_log_states(self):
        vals = {
            'description': 'states changed to %s' % (self.states),
            'patients': self.id
        }
        self.env['hms.patient.log'].create(vals)




