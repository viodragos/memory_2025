# models/project_estimate_line.py

from odoo import models, fields, api

class ProjectEstimateLine(models.Model):
    _name = 'project.estimate.line'
    _description = 'Linie Deviz Proiect'

    project_id = fields.Many2one('project.project', string="Proiect", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Articol", required=True)
    quantity = fields.Float(string="Cantitate", default=1.0)
    unit_price = fields.Float(string="Preț Unitar", related="product_id.list_price", readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)
    deviz_category_id = fields.Many2one('deviz.category', string="Categorie Deviz", required=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price