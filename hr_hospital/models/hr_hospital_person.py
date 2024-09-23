from odoo import models, fields


class Person(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Abstract Person Model'

    name = fields.Char(required=True)
    phone = fields.Char()
    photo = fields.Binary()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
