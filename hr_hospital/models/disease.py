from odoo import models, fields


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(required=True)
    description = fields.Text()
