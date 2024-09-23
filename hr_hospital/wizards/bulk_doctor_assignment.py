from odoo import models, fields

class BulkDoctorAssignment(models.TransientModel):
    _name = 'hr_hospital.bulk_doctor_assignment'
    _description = 'Bulk Doctor Assignment'

    doctor_id = fields.Many2one('hr_hospital.doctor', string='New Doctor', required=True)

    def assign_doctor(self):
        active_ids = self.env.context.get('active_ids', [])
        patients = self.env['hr_hospital.patient'].browse(active_ids)
        patients.write({'doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
