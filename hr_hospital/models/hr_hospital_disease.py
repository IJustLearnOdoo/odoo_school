from odoo import models, fields, api


class Disease(models.Model):
    """
        Represents a disease in the hospital's classification system.

        Implements a hierarchical structure for disease classification with
        parent-child relationships.

        Attributes:
            name (Char): Disease name
            complete_name (Char): Full hierarchical name
            parent_id (Many2one): Parent disease category
            child_ids (One2many): Child disease categories
            description (Text): Disease description
        """
    _name = 'hr_hospital.disease'
    _description = 'Disease'
    _translate = True
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(required=True,
                       translate=True)
    description = fields.Text(translate=True)
    complete_name = fields.Char(
        compute='_compute_complete_name',
        store=True,
        recursive=True,
        translate=True
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
        """
        Computes the complete hierarchical name of the disease.

        The complete name includes all parent categories separated by '/',
        for example: "Cardiovascular/Heart Disease/Arrhythmia"
        """
        for disease in self:
            if disease.parent_id:
                disease.complete_name = '{} / {}'.format(
                    disease.parent_id.complete_name, disease.name
                )
            else:
                disease.complete_name = disease.name
