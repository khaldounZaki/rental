{
    'name': "Rental Application",

    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/equipments_view.xml',
        'views/rental_process_view.xml',
        'views/rental_process_details_view.xml',
        'views/menus.xml',
    ],
    'application': True,
}

