from odoo import models, fields, api, _


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = 'hr_hospital.person'

    specialization = fields.Selection([
        ('neurologist', 'Neurologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('therapist', 'Therapist')
    ], required=True)
    patient_ids = fields.One2many('hr_hospital.patient', 'doctor_id')
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one('hr_hospital.doctor', string='Mentor', domain=[('is_intern', '=', False)])
    user_id = fields.Many2one('res.users', string='Related User')

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise models.ValidationError(_("An intern cannot be selected as a mentor."))
