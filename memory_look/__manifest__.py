{
    'name': 'Memory Look',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Siglă și temă albastră pentru client',
    'depends': ['web'],
    'data': ['views/header_logo.xml',],
    'assets': {
    'web.assets_backend': [
        '/memory_look/static/src/css/memory_look.css',
    ],},
    'installable': True,
    'application': True,
}