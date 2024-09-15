from odoo import models, fields, api
from datetime import date

class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Name', required=True)
    birthday = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    phone = fields.Char(string='Phone')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Observing Doctor')
    visit_ids = fields.One2many('hr_hospital.visit', 'patient_id', string='Visits')

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birthday:
                age = today.year - patient.birthday.year
                if today.month < patient.birthday.month or (today.month == patient.birthday.month and today.day < patient.birthday.day):
                    age -= 1
                patient.age = age
            else:
                patient.age = 0