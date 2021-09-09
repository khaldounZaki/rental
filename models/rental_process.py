from odoo import fields, models , api, _

from odoo.exceptions import ValidationError

import logging
log = logging.getLogger(__name__)
log.info(log)

class rentalProcess(models.Model):
    _name="rental_process"
    _description = "basic information of rental process"
    _rec_name = "process_number"

    process_number = fields.Char(required=True, copy=False, default=lambda self: _('New'), readonly=True, string="Application Number")
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    is_received = fields.Boolean()
    is_returned = fields.Boolean()

    renter_id = fields.Many2one('res.partner', string='Renter', copy=False , required=True)
    rental_process_details_ids = fields.One2many('rental_process_details','rental_process_id'
                                                 , string="Rental Process Details", ondelete='CASCADE')


    @api.constrains('is_received' , 'is_returned')
    def _validate_allow_of_is_received(self):
        log.info('_validate_allow_of_is_received function from %s', log)
        for record in self:
            if (record.is_received == False) and (record.is_returned == True) :
                raise ValidationError("Not allow to activate 'Is Returned' before activate 'Is Received' ")

    @api.constrains('date_from', 'date_to')
    def _validate_date(self):
        log.info('_validate_date function from %s', log)
        for record in self:
            if record.date_from > record.date_to :
                raise ValidationError("'Date From' can not be after 'Date To' ")

    @api.constrains('rental_process_details_ids')
    def _validate_equipment_duplicate(self):
        log.info('_validate_equipment_duplicate function from %s', log)
        for record in self:
            tempList = []
            for rec in record.rental_process_details_ids:
                if rec.equipment_id in tempList:
                    raise ValidationError("You can not choose the same equipment more than one time")
                else:
                    tempList.append(rec.equipment_id )

    # To let sequence one by one
    @api.model
    def create(self, vals):
        log.info('create function from %s', log)
        if vals.get('name', _('New')) == _('New'):
            vals['process_number'] = self.env['ir.sequence'].next_by_code('new_field_value') or _('New')
        res = super(rentalProcess, self).create(vals)
        return res