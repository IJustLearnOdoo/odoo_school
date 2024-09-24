from odoo import models, fields, _
from dateutil.relativedelta import relativedelta


class DiseaseReport(models.TransientModel):
    _name = 'hr_hospital.disease_report'
    _description = 'Disease Report'

    doctor_ids = fields.Many2many('hr_hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr_hospital.disease', string='Diseases')
    date_from = fields.Date(
        string='From Date',
        required=True,
        default=fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='To Date',
        required=True,
        default=fields.Date.today() + relativedelta(day=31)
    )

    def generate_report(self):
        domain = [
            ('visit_id.actual_date', '>=', self.date_from),
            ('visit_id.actual_date', '<=', self.date_to),
        ]
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        diagnoses = self.env['hr_hospital.diagnosis'].search(domain)

        return {
            'name': _('Disease Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.diagnosis',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', diagnoses.ids)],
            'context': {'group_by': 'disease_id'},
        }
