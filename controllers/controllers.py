# -*- coding: utf-8 -*-
# from odoo import http


# class HotelManager(http.Controller):
#     @http.route('/hotel_manager/hotel_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_manager/hotel_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_manager.listing', {
#             'root': '/hotel_manager/hotel_manager',
#             'objects': http.request.env['hotel_manager.hotel_manager'].search([]),
#         })

#     @http.route('/hotel_manager/hotel_manager/objects/<model("hotel_manager.hotel_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_manager.object', {
#             'object': obj
#         })

