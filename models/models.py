# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


# ==================================================
# 1. LOẠI PHÒNG
# ==================================================
class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Loại phòng'

    name = fields.Char(string='Tên loại phòng', required=True)
    code = fields.Char(string='Mã loại')


# ==================================================
# 2. DỊCH VỤ
# ==================================================
class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Dịch vụ khách sạn'

    name = fields.Char(string='Tên dịch vụ', required=True)
    price = fields.Integer(string='Giá dịch vụ')

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Giá dịch vụ phải lớn hơn 0!')
    ]


# ==================================================
# 3. KHÁCH HÀNG
# ==================================================
class HotelCustomer(models.Model):
    _name = 'hotel.customer'
    _description = 'Khách hàng'

    name = fields.Char(string='Tên khách hàng', required=True)
    identity_card = fields.Char(string='CMND/CCCD')
    phone = fields.Char(string='Số điện thoại')

    _sql_constraints = [
        ('identity_unique', 'unique(identity_card)', 'CMND/CCCD đã tồn tại!')
    ]


# ==================================================
# 4. PHÒNG KHÁCH SẠN
# ==================================================
class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Phòng khách sạn'

    name = fields.Char(string='Số phòng', required=True)
    floor = fields.Integer(string='Tầng')
    price_per_night = fields.Integer(string='Giá / đêm')

    status = fields.Selection([
        ('available', 'Trống'),
        ('occupied', 'Đang ở'),
        ('maintenance', 'Bảo trì')
    ], string='Trạng thái', default='available')

    type_id = fields.Many2one(
        'hotel.room.type',
        string='Loại phòng'
    )

    _sql_constraints = [
        ('room_name_unique', 'unique(name)', 'Số phòng đã tồn tại!'),
        ('room_price_positive', 'CHECK(price_per_night > 0)',
         'Giá phòng phải lớn hơn 0!')
    ]


# ==================================================
# 5. BOOKING – PHIẾU ĐẶT PHÒNG
# ==================================================
class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Phiếu đặt phòng'

    code = fields.Char(string='Mã booking')

    check_in = fields.Date(
        string='Ngày nhận phòng',
        default=fields.Date.today
    )
    check_out = fields.Date(string='Ngày trả phòng')

    duration = fields.Integer(
        string='Số đêm',
        compute='_compute_duration',
        store=True
    )

    total_amount = fields.Integer(
        string='Tổng tiền',
        compute='_compute_total_amount',
        store=True
    )

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành')
    ], string='Trạng thái', default='draft')

    customer_id = fields.Many2one(
        'hotel.customer',
        string='Khách hàng',
        required=True
    )

    room_id = fields.Many2one(
        'hotel.room',
        string='Phòng',
        required=True
    )

    service_ids = fields.Many2many(
        'hotel.service',
        string='Dịch vụ đi kèm'
    )

    # -----------------------------
    # COMPUTE
    # -----------------------------
    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0

    @api.depends('duration', 'room_id', 'service_ids')
    def _compute_total_amount(self):
        for record in self:
            room_price = record.room_id.price_per_night if record.room_id else 0
            service_price = sum(record.service_ids.mapped('price'))
            record.total_amount = room_price * record.duration + service_price

    # -----------------------------
    # ONCHANGE
    # -----------------------------
    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id and self.room_id.status == 'maintenance':
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': 'Phòng này đang bảo trì, vui lòng chọn phòng khác!'
                }
            }

    @api.onchange('check_in')
    def _onchange_check_in(self):
        if self.check_in:
            self.check_out = self.check_in + timedelta(days=1)

    # -----------------------------
    # CONSTRAINT
    # -----------------------------
    @api.constrains('check_in', 'check_out')
    def _check_booking_date(self):
        for record in self:
            if record.check_in and record.check_out and record.check_out <= record.check_in:
                raise ValidationError("Ngày trả phòng không hợp lệ!")

    @api.constrains('room_id')
    def _check_room_status(self):
        for record in self:
            if record.room_id.status == 'occupied':
                raise ValidationError("Phòng này đang có khách ở!")

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.room_id.status = 'occupied'

    def action_done(self):
        for record in self:
            record.state = 'done'
            record.room_id.status = 'available'
