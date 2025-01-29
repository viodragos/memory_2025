from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    task_id = fields.Many2one(
        'project.task',
        string="Task",
        help="The task associated with this stock move."
    )