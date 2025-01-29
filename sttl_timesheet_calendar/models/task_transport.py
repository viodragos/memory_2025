from odoo import models, fields, api

class TaskTransport(models.Model):
    _name = 'task.transport'
    _description = 'Task Transport'

    task_id = fields.Many2one('project.task', string="Task", required=True, ondelete="cascade", default=lambda self: self.env.context.get('default_task_id'))
    service_id = fields.Many2one('product.product', string="Transport Service", required=True, domain="[('type', '=', 'service'), ('is_transport', '=', True)]")
    quantity = fields.Float(string="Distance (Km)", required=True)
    unit_price = fields.Float(string="Unit Price", related="service_id.list_price", readonly=True)
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.unit_price