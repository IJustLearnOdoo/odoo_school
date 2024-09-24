from odoo import models, fields, api


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(required=True)
    complete_name = fields.Char(
        compute='_compute_complete_name',
        store=True,
        recursive=True
    )
    parent_id = fields.Many2one(
        'hr_hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='cascade'
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        'hr_hospital.disease',
        'parent_id',
        string='Child Diseases'
    )
    description = fields.Text()

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for disease in self:
            if disease.parent_id:
                disease.complete_name = '{} / {}'.format(
                    disease.parent_id.complete_name, disease.name
                )
            else:
                disease.complete_name = disease.name
