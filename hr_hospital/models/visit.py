from odoo import models, fields

class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    date = fields.Date(string='Visit Date', required=True)
    disease_id = fields.Many2one('hr_hospital.disease', string='Diagnosed Disease')
    notes = fields.Text(string='Notes')
