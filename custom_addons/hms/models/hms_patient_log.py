from  odoo import models, fields,api

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'

    description = fields.Text()
    patients = fields.Many2one('hms.patient')