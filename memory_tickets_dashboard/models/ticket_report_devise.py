from odoo import models, tools, fields

class TicketReportDevise(models.Model):
    _name = 'ticket.report.devise'
    _auto = False  # Indică faptul că este o vedere SQL
    _description = "Raport Tichete"

    id = fields.Integer(string="ID", readonly=True)
    ticket_id = fields.Many2one('ticket.helpdesk', string="Tichet", readonly=True)
    ticket_name = fields.Char(string="Nume Tichet", readonly=True)
    ticket_subject = fields.Char(string="Subiect Tichet", readonly=True)
    stage = fields.Char(string="Stadiu", readonly=True)
    customer_id = fields.Many2one('res.partner', string="Client", readonly=True)
    customer_name = fields.Char(string="Nume Client", readonly=True)
    project_id = fields.Many2one('project.project', string="Proiect", readonly=True)
    project_name = fields.Char(string="Nume Proiect", readonly=True)
    task_id = fields.Many2one('project.task', string="Sarcină", readonly=True)
    task_name = fields.Char(string="Nume Sarcină", readonly=True)
    
    # Date despre timp
    tip_document = fields.Char(string="Tip Document", readonly=True)
    numar_intern = fields.Char(string="Număr Intern", readonly=True)
    date_deadline = fields.Date(string="Termen Limită", readonly=True)
    ticket_billed = fields.Boolean(string="Facturat", readonly=True)

    # Costuri manoperă
    total_hours = fields.Float(string="Ore Lucrate", readonly=True)
    cost_manopera = fields.Float(string="Cost Manoperă", readonly=True)
    venit_manopera = fields.Float(string="Venit Manoperă", readonly=True)

    # Costuri materiale
    total_material_qty = fields.Float(string="Cantitate Materiale", readonly=True)
    cost_material = fields.Float(string="Cost Materiale", readonly=True)
    venit_material = fields.Float(string="Venit Materiale", readonly=True)

    # Costuri transport
    total_transport_qty = fields.Float(string="Km Transport", readonly=True)
    cost_transport = fields.Float(string="Cost Transport", readonly=True)
    venit_transport = fields.Float(string="Venit Transport", readonly=True)

    # Ordine de vânzare
    so_amount = fields.Float(string="Valoare SO (Fără TVA)", readonly=True)
    so_tax = fields.Float(string="TVA SO", readonly=True)
    so_total = fields.Float(string="Valoare SO (Total)", readonly=True)
    so_count = fields.Integer(string="Nr. Ordine de Vânzare", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW "ticket_report_devise" AS 
            SELECT 
                ROW_NUMBER() OVER() AS id,  -- Adăugăm un ID unic         
                t.id AS "ticket_id",
                t.name AS "ticket_name",
                t.subject AS "ticket_subject",
                ts.name AS "stage",
                t.customer_id,
                rp.name AS "customer_name",
                t.project_id,
                COALESCE(
                    NULLIF(jsonb_extract_path_text(pp.name::jsonb, 'ro_RO'), ''), 
                    NULLIF(jsonb_extract_path_text(pp.name::jsonb, 'en_US'), ''), 
                    'n/a'
                ) AS "project_name",
                pt.id AS "task_id",
                pt.name AS "task_name",
                pt.tip_document,
                pt.numar_intern,
                pt.date_deadline,
                pt.ticket_billed,

                -- Manoperă (agregată la nivel de sarcină)
                COALESCE(SUM(timesheet.total_hours), 0) AS "total_hours",
                COALESCE(SUM(timesheet.cost_manopera), 0) AS "cost_manopera",
                COALESCE(SUM(timesheet.venit_manopera), 0) AS "venit_manopera",

                -- Materiale (agregate la nivel de sarcină)
                COALESCE(SUM(materials.total_material_qty), 0) AS "total_material_qty",
                COALESCE(SUM(materials.cost_material), 0) AS "cost_material",
                COALESCE(SUM(materials.venit_material), 0) AS "venit_material",

                -- Transport (agregat la nivel de sarcină)
                COALESCE(SUM(transport.total_transport_qty), 0) AS "total_transport_qty",
                COALESCE(SUM(transport.cost_transport), 0) AS "cost_transport",
                COALESCE(SUM(transport.venit_transport), 0) AS "venit_transport",

                -- Detalii ordine de vânzare (dacă există)
                COALESCE(SUM(so.amount_untaxed), 0) AS "so_amount",
                COALESCE(SUM(so.amount_tax), 0) AS "so_tax",
                COALESCE(SUM(so.amount_total), 0) AS "so_total",
                COUNT(DISTINCT so.id) AS "so_count"

            FROM "ticket_helpdesk" t
            LEFT JOIN "public"."project_task_ticket_helpdesk_rel" ptth ON t.id = ptth.ticket_helpdesk_id
            LEFT JOIN "project_task" pt ON ptth.project_task_id = pt.id

            -- Pontaje (grupate la nivel de sarcină)
            LEFT JOIN (
                SELECT aal.task_id, 
                       SUM(aal.unit_amount) AS total_hours,
                       SUM(ip.standard_price * aal.unit_amount) AS cost_manopera,
                       SUM(pt_manopera.list_price * aal.unit_amount) AS venit_manopera
                FROM "account_analytic_line" aal
                LEFT JOIN "sale_order_line" sol ON sol.id = aal.so_line
                LEFT JOIN "product_product" pp_manopera ON sol.product_id = pp_manopera.id
                LEFT JOIN "product_template" pt_manopera ON pp_manopera.product_tmpl_id = pt_manopera.id
                LEFT JOIN (
                    SELECT res_id, value_float AS standard_price
                    FROM "ir_property"
                    WHERE name = 'standard_price'
                ) ip ON ip.res_id = CONCAT('product.product,', pp_manopera.id)
                GROUP BY aal.task_id
            ) timesheet ON timesheet.task_id = pt.id

            -- Legătura cu ordinele de vânzare
            LEFT JOIN "sale_order" so ON so.id = pt.sale_order_id

            -- Materiale (grupate la nivel de sarcină)
            LEFT JOIN (
                SELECT tm.task_id, 
                       SUM(tm.quantity) AS total_material_qty,
                       SUM(ipmat.standard_price * tm.quantity) AS cost_material,
                       SUM(pt_material.list_price * tm.quantity) AS venit_material
                FROM "task_material" tm
                LEFT JOIN "product_product" pp_material ON tm.product_id = pp_material.id 
                LEFT JOIN "product_template" pt_material ON pp_material.product_tmpl_id = pt_material.id
                LEFT JOIN (
                    SELECT res_id, value_float AS standard_price
                    FROM "ir_property"
                    WHERE name = 'standard_price'
                ) ipmat ON ipmat.res_id = CONCAT('product.product,', pp_material.id)
                GROUP BY tm.task_id
            ) materials ON materials.task_id = pt.id

            -- Transport (grupat la nivel de sarcină)
            LEFT JOIN (
                SELECT tt.task_id, 
                       SUM(tt.quantity) AS total_transport_qty,
                       SUM(iptra.standard_price * tt.quantity) AS cost_transport,
                       SUM(pt_transport.list_price * tt.quantity) AS venit_transport
                FROM "task_transport" tt
                LEFT JOIN "product_product" pp_transport ON tt.service_id = pp_transport.id 
                LEFT JOIN "product_template" pt_transport ON pp_transport.product_tmpl_id = pt_transport.id
                LEFT JOIN (
                    SELECT res_id, value_float AS standard_price
                    FROM "ir_property"
                    WHERE name = 'standard_price'
                ) iptra ON iptra.res_id = CONCAT('product.product,', pp_transport.id)
                GROUP BY tt.task_id
            ) transport ON transport.task_id = pt.id

            -- Alte date
            LEFT JOIN "res_partner" rp ON rp.id = t.customer_id
            LEFT JOIN "project_project" pp ON pp.id = t.project_id
            LEFT JOIN "ticket_stage" ts ON ts.id = t.stage_id

            GROUP BY 
                t.id, t.name, t.subject, ts.name, t.customer_id, rp.name, t.project_id, pp.name, 
                pt.id, pt.name, pt.tip_document, pt.numar_intern, pt.date_deadline, pt.ticket_billed

            ORDER BY t.id, pt.id;
        """)
