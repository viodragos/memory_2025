# models/deviz_category.py

from odoo import models, fields

class DevizCategory(models.Model):
    _name = 'deviz.category'
    _description = 'Categorie Deviz'

    name = fields.Char(string="Nume Categorie", required=True, translate=True)
    code = fields.Char(string="Cod", help="Cod scurt pentru raportări")
    color = fields.Integer(string="Culoare")  # util pentru kanban/charts dacă vreodată :)