from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_transport = fields.Boolean(
        string="Is Transport Service",
        help="Indicates if the service is a transport service.",
        related='product_variant_ids.is_transport',
        readonly=False,  # Permite editarea câmpului
        store=True  # Asigură-te că este stocat pentru performanță
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_transport = fields.Boolean(
        string="Is Transport Service",
        help="Indicates if the service is a transport service."
    )