from odoo import fields, models,api

from . import functions

import logging
log = logging.getLogger(__name__)
log.info(log)

class equipmentProperty(models.Model):
    _name="equipment_property"
    _description = "equipment details and properties"

    name = fields.Char(required=True)
    equipment_number = fields.Char(required=True)
    equipment_description = fields.Text(string="Description")

    state = fields.Selection(selection=[('available','Available'),
                                        ('requested' , 'Requested'),
                                        ('rented', 'Rented'),
                                        ('late', 'Late')],
                             required=True, copy=False, compute="_compute_state",
                             default='available' , string="Rent Status", readonly= True)


    #the next field is added  to let (state) be stored in order to let filter work
    StoredState = fields.Selection(selection=[('available','Available'),
                                        ('requested' , 'Requested'),
                                        ('rented', 'Rented'),
                                        ('late', 'Late')],default='available')

    date_from = fields.Date(readonly=True)
    return_date = fields.Date(readonly=True)

    rental_process_details_ids = fields.One2many('rental_process_details','equipment_id', string="Rental Process Details")
    renter_id = fields.Many2one('res.partner', string='Renter', readonly=True)


    _sql_constraints = [('check_unique_name', 'UNIQUE (equipment_number) ', 'Equipment Number Must Be Unique')]


    # the next function let equipment appear in <name>(<state>) pattern
    def name_get(self):
        log.info('name_get function from %s', log)
        result = []
        for record in self:
            name = record.name + " ("+ record.state +")"
            result.append((record.id,name))
        return result

    @api.depends("rental_process_details_ids")
    def _compute_state(self):
        log.info('_compute_state function from %s', log)
        for record in self:
            theState = 'available'
            theRenter = None
            theReturnDate = None
            theDateFrom = None
            if record.rental_process_details_ids:
                for rec in record.rental_process_details_ids:
                    if rec.rental_process_id != functions.record_flag :
                        theState = functions.choose_state(functions.get_record_state(rec), theState )
                        if theState == 'rented' or theState == 'late':
                            theRenter = rec.rental_process_id.renter_id
                            theReturnDate = rec.rental_process_id.date_to
                            theDateFrom = rec.rental_process_id.date_from
                    else:
                        continue
            else:
                theState= "available"
            record.state = theState
            record.StoredState = theState
            record.renter_id = theRenter
            record.return_date = theReturnDate
            record.date_from = theDateFrom










