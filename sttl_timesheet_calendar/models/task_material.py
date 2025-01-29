from odoo import models, fields, api

class TaskMaterial(models.Model):
    _name = 'task.material'
    _description = 'Task Material'

    task_id = fields.Many2one('project.task', string="Task", required=True, ondelete="cascade", default=lambda self: self.env.context.get('default_task_id'))
    product_id = fields.Many2one('product.product', string="Material", required=True, domain="[('type', 'in', ['product', 'consu'])]")
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Unit Price", related="product_id.list_price", readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)
    stock_move_id = fields.Many2one('stock.move', string="Stock Move", readonly=True)  # Câmp nou

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price

   


    