from odoo import models, api

class TicketHelpDesk(models.Model):
    _inherit = 'ticket.helpdesk'

    @api.model
    def get_dashboard_data(self):
        tickets = self.search([])
        total_ore = 0.0
        cost_manopera = 0.0
        venit_manopera = 0.0

        total_materiale_fisa = 0.0
        total_materiale_pick = 0.0
        discrepanta_materiale = 0.0

        total_km = 0.0
        cost_transport = 0.0

        venit_total_facturi = 0.0

        for ticket in tickets:
            # Sarcini legate de tichet
            tasks = self.env['project.task'].search([('ticket_id', '=', ticket.id)])

            for task in tasks:
                # Timesheets - manoperă
                timesheets = self.env['account.analytic.line'].search([('task_id', '=', task.id)])
                for ts in timesheets:
                    ore = ts.unit_amount
                    total_ore += ore
                    if ts.so_line:
                        produs = ts.so_line.product_id
                        cost_manopera += produs.standard_price * ore
                        venit_manopera += produs.list_price * ore

                # Materiale din fișa de sarcină
                for material_line in task.material_line_ids:
                    total_materiale_fisa += material_line.product_uom_qty * material_line.product_id.standard_price

                # Materiale din pick-uri
                stock_moves = self.env['stock.move'].search([('task_id', '=', task.id)])
                for move in stock_moves:
                    total_materiale_pick += move.product_uom_qty * move.product_id.standard_price

                # Transport
                for transport_line in task.transport_line_ids:
                    km = transport_line.distance_km
                    total_km += km
                    if transport_line.service_id:
                        cost_transport += km * transport_line.service_id.standard_price

            # Facturi legate direct de tichet
            venit_total_facturi += sum(ticket.invoice_ids.mapped('amount_total'))

        # Calcul discrepanță materiale
        discrepanta_materiale = total_materiale_fisa - total_materiale_pick

        return {
            'total_ore': total_ore,
            'cost_manopera': cost_manopera,
            'venit_manopera': venit_manopera,
            'total_materiale_fisa': total_materiale_fisa,
            'total_materiale_pick': total_materiale_pick,
            'discrepanta_materiale': discrepanta_materiale,
            'total_km': total_km,
            'cost_transport': cost_transport,
            'venit_total_facturi': venit_total_facturi,
            'profit_total': venit_total_facturi - (cost_manopera + total_materiale_pick + cost_transport),
        }