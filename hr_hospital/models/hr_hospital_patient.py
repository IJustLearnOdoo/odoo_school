from datetime import date
from odoo import models, fields, api


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = 'hr_hospital.person'

    birthday = fields.Date(required=True)
    age = fields.Integer(compute='_compute_age', store=True)
    doctor_id = fields.Many2one('hr_hospital.doctor')
    visit_ids = fields.One2many('hr_hospital.visit', 'patient_id')
    passport_data = fields.Char()
    contact_person = fields.Char()

    @api.model
    def _update_all_ages(self):
        patients = self.search([])
        for patient in patients:
            patient._compute_age()

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birthday:
                age = today.year - patient.birthday.year
                if (today.month < patient.birthday.month or
                        (today.month == patient.birthday.month and
                         today.day < patient.birthday.day)):
                    age -= 1
                patient.age = age
            else:
                patient.age = 0
