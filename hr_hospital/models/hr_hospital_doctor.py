from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError


class Doctor(models.Model):
    """
        Represents a doctor in the hospital management system.

        This model stores information about doctors, including their
        specialization,
        patients, and mentor/intern relationships.

        Attributes:
            name (Char): The doctor's full name
            specialization (Selection): Medical specialization
            patient_ids (One2many): Related patients
            is_intern (Boolean): Whether the doctor is an intern
            mentor_id (Many2one): Senior doctor mentoring this doctor if intern
            intern_ids (One2many): Interns being mentored by this doctor
            user_id (Many2one): Related user in the system
            visit_ids (One2many): All visits associated with this doctor
    """
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.person']

    specialization = fields.Selection([
        ('neurologist', 'Neurologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('therapist', 'Therapist'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('gastroenterologist', 'Gastroenterologist'),
        ('oncologist', 'Oncologist'),
        ('pediatrician', 'Pediatrician'),
        ('radiologist', 'Radiologist'),
        ('urologist', 'Urologist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('orthopedic_surgeon', 'Orthopedic Surgeon')
    ], required=True)

    patient_ids = fields.One2many('hr_hospital.patient',
                                  'doctor_id')
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(
        'hr_hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )
    intern_ids = fields.One2many('hr_hospital.doctor',
                                 'mentor_id',
                                 string='Interns')
    user_id = fields.Many2one('res.users',
                              string='Related User')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    visit_ids = fields.One2many('hr_hospital.visit',
                                'doctor_id', string='Visits')
    color = fields.Integer(string='Color Index')

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        """
        Validates mentor-intern relationships.

        Ensures that:
            1. An intern cannot be a mentor
            2. A doctor can't mentor themselves

        Raises:
            ValidationError: If validation fails
        """
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

    def action_view_visits(self):
        """
        Opens a view displaying all visits for this doctor.

       Returns:
           dict: Action dictionary for the visits view
       """
        self.ensure_one()
        return {
            'name': _('Doctor Visits'),
            'view_mode': 'tree,form',
            'res_model': 'hr_hospital.visit',
            'domain': [('doctor_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_doctor_id': self.id},
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            'name': _('Create Visit'),
            'view_mode': 'form',
            'res_model': 'hr_hospital.visit',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }

    def action_open_mentor_form(self):
        self.ensure_one()
        action = {'type': 'ir.actions.act_window_close'}

        action.update({
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.doctor',
            'res_id': self.mentor_id.id,
            'view_mode': 'form',
        })
        return action
