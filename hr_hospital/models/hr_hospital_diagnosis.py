from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        'hr_hospital.visit',
        string='Visit',
        required=True
    )
    disease_id = fields.Many2one(
        'hr_hospital.disease',
        required=True
    )
    description = fields.Text(
        string='Treatment Description'
    )
    is_approved = fields.Boolean(
        string='Approved'
    )
    needs_approval = fields.Boolean(
        compute='_compute_needs_approval',
        store=True
    )

    @api.depends(
        'visit_id.doctor_id.is_intern',
        'visit_id.doctor_id.mentor_id'
    )
    def _compute_needs_approval(self):
        for diagnosis in self:
            doctor = diagnosis.visit_id.doctor_id
            diagnosis.needs_approval = (doctor.is_intern
                                        and bool(doctor.mentor_id))

    @api.constrains('is_approved')
    def _check_approval(self):
        for diagnosis in self:
            if diagnosis.is_approved and diagnosis.needs_approval:
                approver = self.env['hr_hospital.doctor'].search(
                    [('user_id', '=', self.env.uid)], limit=1)
                if not approver:
                    raise ValidationError(_(
                        "Only doctors can approve diagnoses."
                    ))
                if approver.is_intern and approver.mentor_id:
                    raise ValidationError(_(
                        "Interns cannot approve diagnoses."
                    ))

    @api.model
    def create(self, vals):
        current_doctor = self.env['hr_hospital.doctor'].search(
            [('user_id', '=', self.env.uid)], limit=1)
        if current_doctor:
            if current_doctor.is_intern and current_doctor.mentor_id:
                vals['is_approved'] = False
            else:
                vals['is_approved'] = True

        diagnosis = super(Diagnosis, self).create(vals)
        if diagnosis.needs_approval and not diagnosis.is_approved:
            diagnosis._check_approval()
        return diagnosis

    def write(self, vals):
        result = super(Diagnosis, self).write(vals)
        if 'is_approved' in vals:
            self._check_approval()
        return result
