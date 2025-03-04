from odoo import models, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model
    def get_dashboard_data(self):
        return {
            'total': self.search_count([]),
            'deschise': self.search_count([('stage_id.name', '=', 'Nou')]),
            'in_curs': self.search_count([('stage_id.name', '=', 'În curs')]),
            'finalizate': self.search_count([('stage_id.name', '=', 'Finalizat')]),
        }