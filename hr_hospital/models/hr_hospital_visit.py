from odoo import models, fields


class HospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr_hospital.patient', required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', required=True)
    date = fields.Date(required=True)
    disease_id = fields.Many2one('hr_hospital.disease')
    notes = fields.Text()
