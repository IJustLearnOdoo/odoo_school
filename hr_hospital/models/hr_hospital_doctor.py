from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError


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
    mentor_id = fields.Many2one(
        'hr_hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )
    user_id = fields.Many2one('res.users', string='Related User')

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError(
                    _("An intern cannot be selected as a mentor.")
                )

    def write(self, vals):
        if not self.env.is_admin():
            if 'user_id' in vals or 'is_intern' in vals or 'mentor_id' in vals:
                raise AccessError(
                    _("Only administrators can modify 'Related User', "
                      "'Is Intern', and 'Mentor' fields.")
                )
        return super(Doctor, self).write(vals)

    @api.model
    def create(self, vals):
        if not self.env.is_admin() and (
                'user_id' in vals or
                'is_intern' in vals or
                'mentor_id' in vals):
            raise AccessError(
                _("Only administrators can set 'Related User', "
                  "'Is Intern', and 'Mentor' fields.")
            )
        return super(Doctor, self).create(vals)

    def unlink(self):
        if not self.env.is_admin():
            raise AccessError(
                _("Only administrators can delete doctor records.")
            )
        return super(Doctor, self).unlink()

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(Doctor, self).fields_get(allfields, attributes)
        if not self.env.is_admin():
            for field in ['is_intern', 'user_id', 'mentor_id']:
                if field in res:
                    res[field]['readonly'] = True
        return res
