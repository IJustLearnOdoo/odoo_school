from odoo import models, fields


class DoctorReassignWizard(models.TransientModel):
    _name = 'hr_hospital.doctor_reassign_wizard'
    _description = 'Doctor Reassignment Wizard'

    doctor_id = fields.Many2one(
        'hr_hospital.doctor',
        string='New Doctor',
        required=True
    )

    def action_reassign_doctor(self):
        patient_ids = self.env.context.get('active_ids', [])
        patients = self.env['hr_hospital.patient'].browse(patient_ids)
        patients.write({'doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
