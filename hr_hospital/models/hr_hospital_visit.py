from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Visit(models.Model):
    """
   Represents a medical visit in the hospital system.

   Tracks appointments between doctors and patients, including scheduling
   and diagnosis information.

   Attributes:
       patient_id (Many2one): Related patient
       doctor_id (Many2one): Attending doctor
       scheduled_date (Datetime): Planned visit time
       actual_date (Datetime): Actual visit time
       status (Selection): Visit status (scheduled/completed/cancelled)
       diagnosis_ids (One2many): Diagnoses made during the visit
   """
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr_hospital.patient', required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', required=True)
    scheduled_date = fields.Datetime(
        required=True,
        string='Scheduled Date and Time'
    )
    actual_date = fields.Datetime(string='Actual Date and Time')
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled', required=True)
    diagnosis_ids = fields.One2many(
        'hr_hospital.diagnosis',
        'visit_id',
        string='Diagnoses'
    )

    @api.constrains('patient_id', 'doctor_id', 'scheduled_date')
    def _check_duplicate_visit(self):
        """
        Prevents duplicate visits for the same doctor-patient pair on same day.

        Raises:
            ValidationError: If a duplicate visit is detected
        """
        for visit in self:
            next_day = visit.scheduled_date + timedelta(days=1)
            duplicate = self.search([
                ('patient_id', '=', visit.patient_id.id),
                ('doctor_id', '=', visit.doctor_id.id),
                ('scheduled_date', '>=', visit.scheduled_date.date()),
                ('scheduled_date', '<', next_day.date()),
                ('id', '!=', visit.id)
            ])
            if duplicate:
                raise ValidationError(_(
                    "A visit for this patient with this doctor "
                    "already exists on the same day."
                ))

    def write(self, vals):
        for visit in self:
            if visit.status == 'completed':
                protected_fields = [
                    'scheduled_date',
                    'actual_date',
                    'doctor_id'
                ]
                if any(field in vals for field in protected_fields):
                    raise ValidationError(_(
                        "You cannot modify the date, time, or doctor "
                        "for a completed visit."
                    ))
        return super(Visit, self).write(vals)

    def unlink(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError(_(
                    "You cannot delete a visit that has diagnoses."
                ))
        return super(Visit, self).unlink()
