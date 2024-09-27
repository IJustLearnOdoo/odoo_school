from datetime import date
from odoo import models, fields, api


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = 'hr_hospital.person'

    birthday = fields.Date(required=True)
    age = fields.Integer(compute='_compute_age', store=True,
                         group_operator="")
    doctor_id = fields.Many2one('hr_hospital.doctor')
    visit_ids = fields.One2many('hr_hospital.visit', 'patient_id')
    diagnosis_ids = fields.One2many('hr_hospital.diagnosis',
                                    'patient_id', string='Diagnoses')
    passport_data = fields.Char()
    contact_person = fields.Char()
    diagnosis_history_ids = fields.One2many(
        'hr_hospital.diagnosis',
        'patient_id',
        string='Diagnosis History'
    )

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

    def action_view_visits(self):
        self.ensure_one()
        return {
            'name': 'Patient Visits',
            'view_mode': 'tree,form',
            'res_model': 'hr_hospital.visit',
            'domain': [('patient_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id': self.id},
        }

    def action_create_visit(self):
        return {
            'name': 'Create Visit',
            'view_mode': 'form',
            'res_model': 'hr_hospital.visit',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }
