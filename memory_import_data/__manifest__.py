{
    'name': 'Custom Data Import',
    'version': '1.0',
    'summary': 'Import demo data for partners, departments, jobs, and employees',
    'category': 'Tools',
    'author': 'Your Name',
    'depends': ['base', 'hr', 'product'],
    'data': [
        'data/hr_department_demo.xml',
        'data/hr_job_demo.xml',
        'data/res_partner_demo.xml',
        'data/hr_employee_demo.xml',
        'data/res_users_demo.xml',
        'data/product_demo.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
