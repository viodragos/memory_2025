from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string="Source Warehouse",
        help="Warehouse associated with this project as the source of materials."
    )
    destination_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string="Destination Warehouse",
        help="Warehouse associated with this project as the destination for materials."
    )
    location_source_id = fields.Many2one(
        'stock.location',
        string="Source Location",
        help="Default source location for stock moves associated with this project."
    )
    location_dest_id = fields.Many2one(
        'stock.location',
        string="Destination Location",
        help="Default destination location for stock moves associated with this project."
    )