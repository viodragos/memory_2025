from odoo import models, fields, api
import logging


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)

        for task in self:
            # Determinăm locațiile
            location_id = (
                task.project_id.location_source_id.id
                if task.project_id.location_source_id
                else self.env['stock.location'].search([('name', '=', 'Magazie')], limit=1).id
            )
            location_dest_id = (
                task.project_id.location_dest_id.id
                if task.project_id.location_dest_id
                else self.env.ref('stock.stock_location_customer').id
            )

            # Verificăm dacă există un picking pentru sarcina curentă
            picking = self.env['stock.picking'].search([
                ('origin', '=', f"Task: {task.name}"),
                ('state', '!=', 'cancel'),
            ], limit=1)

            if not picking:
                # Creăm un picking nou pentru sarcina curentă
                picking = self.env['stock.picking'].create({
                    'partner_id': task.project_id.partner_id.id if task.project_id.partner_id else None,
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'scheduled_date': task.date_deadline or fields.Datetime.now(),
                    'picking_type_id': self.env['stock.picking.type'].search([
                        ('code', '=', 'outgoing'),
                        ('warehouse_id', '=', task.project_id.warehouse_id.id if task.project_id.warehouse_id else None),
                    ], limit=1).id,
                    'origin': f"Task: {task.name}",
                })

            # Ștergem doar mișcările asociate sarcinii curente
            picking.move_ids_without_package.filtered(lambda m: m.task_id == task).unlink()

            # Adăugăm mișcările în picking
            for material in task.material_ids:
                self.env['stock.move'].create({
                    'name': f"Material Consumption for Task: {task.name}",
                    'product_id': material.product_id.id,
                    'product_uom_qty': material.quantity,
                    'product_uom': material.product_id.uom_id.id,
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'picking_id': picking.id,
                    'task_id': task.id,
                })

            # Validăm picking-ul doar dacă are mișcări
            if picking.state not in ['done', 'cancel']:
                if picking.move_ids_without_package:
                    picking.action_confirm()  # Confirmăm picking-ul
                  #  picking.button_validate()  # Validăm picking-ul
                else:
                    logging.warning(f"Skipping validation for empty picking {picking.id}.")

        return res