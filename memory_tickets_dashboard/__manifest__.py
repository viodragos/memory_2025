{
    'name': 'Memory Tickets Dashboard',
    'version': '1.0',
    'category': 'Helpdesk',
    'author' : 'Viorel Dragos',
    'summary': 'Dashboard personalizat pentru tichete',
    'depends': ['odoo_website_helpdesk'],
    'assets': {
        'web.assets_backend': [
            '/memory_tickets_dashboard/static/src/js/dashboard.js',
            '/memory_tickets_dashboard/static/src/xml/dashboard.xml',
            'https://cdn.jsdelivr.net/npm/chart.js',  # Adăugăm Chart.js din CDN
        ],
    },
    'data': [
        'views/actions.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}