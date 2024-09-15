from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Selection([('neurologist', 'Neurologist'), ('psychiatrist', 'Psychiatrist'), ('therapist', 'Therapist')], string='Specialization')
    phone = fields.Char(string='Phone')
    patient_ids = fields.One2many('hr_hospital.patient', 'doctor_id', string='Patients')
