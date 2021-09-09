from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from . import functions

import logging
log = logging.getLogger(__name__)
log.info(log)


class rentalProcessDetails(models.Model):
    _name="rental_process_details"
    _description = "the details of rental operation"
    _rec_name = "equipment_id"

    rental_process_id = fields.Many2one("rental_process", string="Rental Process", ondelete='CASCADE')
    equipment_id = fields.Many2one("equipment_property", string="Equipment Property")


    @api.constrains('equipment_id')
    def _check_equipment_state(self):
        log.info('_check_equipment_state from %s', log)
        for record in self:
            functions.record_flag = record.rental_process_id
            theState= record.equipment_id.state
            if theState != 'available' :
                functions.record_flag = -1
                raise ValidationError("One or more Equipments are not available to rent")
            functions.record_flag = -1


