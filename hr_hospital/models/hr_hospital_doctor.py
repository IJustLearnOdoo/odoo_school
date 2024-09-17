from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(required=True)
    specialization = fields.Selection(
        [
            ('neurologist', 'Neurologist'),
            ('psychiatrist', 'Psychiatrist'),
            ('therapist', 'Therapist')
        ]
    )
    phone = fields.Char()
    patient_ids = fields.One2many('hr_hospital.patient', 'doctor_id')
