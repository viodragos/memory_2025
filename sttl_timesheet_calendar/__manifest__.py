# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

{
    'name': 'Timesheet Calendar',
    'version': '17.0.1.0',
    'author': 'Silver Touch Technologies Limited',
    'website': 'https://www.silvertouch.com',
    'license': 'LGPL-3',
    'support': 'service@silvertouch.com',
    'category': 'Analytic',
    'summary': 'Allows to Fill timesheet from calender view',
    'price': 00,
    'currency': 'EUR',
    'depends': [
        'base',
        'hr_timesheet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_timesheet_view.xml',
        'views/product_transport.xml',
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
