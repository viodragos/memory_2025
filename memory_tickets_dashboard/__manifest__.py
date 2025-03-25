{
    'name': 'Memory Tickets Dashboard',
    'version': '1.0',
    'category': 'Helpdesk',
    'author' : 'Viorel Dragos',
    'summary': 'Dashboard personalizat pentru tichete',
    'depends': ['odoo_website_helpdesk'],
    'data': [
        'views/dashboard.xml',
        'views/actions.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'views/project_edit_project.xml',
       
    ],
    'installable': True,
    'application': True,
}