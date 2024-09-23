from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one('hr_hospital.visit', string='Visit', required=True)
    disease_id = fields.Many2one('hr_hospital.disease', required=True)
    description = fields.Text(string='Treatment Description')
    is_approved = fields.Boolean(string='Approved')
    needs_approval = fields.Boolean(compute='_compute_needs_approval', store=True)

    @api.depends('visit_id.doctor_id.is_intern')
    def _compute_needs_approval(self):
        for diagnosis in self:
            diagnosis.needs_approval = diagnosis.visit_id.doctor_id.is_intern

    @api.constrains('is_approved')
    def _check_approval(self):
        for diagnosis in self:
            if diagnosis.is_approved and diagnosis.needs_approval:
                doctor = diagnosis.visit_id.doctor_id
                if doctor.is_intern and doctor.mentor_id:
                    # Перевіряємо, чи поточний користувач є ментором
                    if self.env.user.id != doctor.mentor_id.user_id.id:
                        raise ValidationError(_("Only the mentor can approve an intern's diagnosis."))
                elif doctor.is_intern:
                    raise ValidationError(_("Intern's diagnosis needs approval from a mentor."))
