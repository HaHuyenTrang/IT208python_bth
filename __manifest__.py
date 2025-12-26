# -*- coding: utf-8 -*-
{
    'name': "Hotel_manager",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',

        # SEARCH VIEWS PHẢI LOAD TRƯỚC
        'views/hotel_booking_search.xml',

        # FORM + TREE
        'views/hotel_booking_views.xml',
        'views/hotel_customer_views.xml',

        # ACTION + MENU LOAD SAU CÙNG
        'views/actions.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'license': "LGPL-3"
}
