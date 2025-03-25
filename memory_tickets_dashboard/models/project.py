from odoo import models, fields, api
from collections import defaultdict

class ProjectProject(models.Model):
    _inherit = 'project.project'

    estimate_line_ids = fields.One2many('project.estimate.line', 'project_id', string="Deviz Proiect")
    devise_summary = fields.Html(string="Centralizare pe capitole", compute="_compute_devise_summary")

    @api.depends('estimate_line_ids', 'estimate_line_ids.subtotal', 'estimate_line_ids.deviz_category_id')
    def _compute_devise_summary(self):
        for project in self:
            totals = defaultdict(float)
            total_general = 0.0

            for line in project.estimate_line_ids:
                category = line.deviz_category_id.name or 'Fără categorie'
                totals[category] += line.subtotal
                total_general += line.subtotal

            if not totals:
                project.devise_summary = "<p>Nu există linii în deviz.</p>"
                continue

            html = """
                <table class="table table-sm" style="width: 60%; margin-top: 10px;">
                    <thead>
                        <tr>
                            <th>Capitol</th>
                            <th style="text-align: right;">Valoare (lei)</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for category, value in totals.items():
                html += f"""
                    <tr>
                        <td>{category}</td>
                        <td style="text-align: right;">{value:,.2f}</td>
                    </tr>
                """
            html += f"""
                    <tr style="font-weight: bold; border-top: 1px solid #ccc;">
                        <td>Total general</td>
                        <td style="text-align: right;">{total_general:,.2f}</td>
                    </tr>
            """
            html += "</tbody></table>"

            project.devise_summary = html