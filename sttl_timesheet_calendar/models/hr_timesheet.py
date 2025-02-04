# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime
import logging

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    from_time = fields.Char("From Time (hh:mm)")
    to_time = fields.Char("To Time (hh:mm)")
    from_date = fields.Datetime("From Date")
    to_date = fields.Datetime("To Date")
     # Adăugăm câmpul so_line pentru testare (dacă nu există deja)
    so_line = fields.Many2one('sale.order.line', string="SO Line", ondelete="set null")
    
    def _compute_rounded_duration(self, from_date, to_date):
        """ Calculates the duration between two dates, rounded to two decimal places """
        if from_date and to_date:
            time_diff = (to_date - from_date).total_seconds() / 3600
            return round(time_diff, 2)
        return 0.0

    @api.onchange('from_time', 'to_time', 'date')
    def _onchange_times(self):
        """ Update from_date and to_date based on the date and time inputs, then calculate duration """
        time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')

        # Validate time format for both from_time and to_time
        if self.from_time and not time_pattern.match(self.from_time):
            raise ValidationError(_("The 'From Time' must be in the format 'hh:mm'."))
        if self.to_time and not time_pattern.match(self.to_time):
            raise ValidationError(_("The 'To Time' must be in the format 'hh:mm'."))

        if self.from_time and self.to_time and self.date:
            from_hours, from_minutes = map(int, self.from_time.split(':'))
            to_hours, to_minutes = map(int, self.to_time.split(':'))

            # Convert self.date to a datetime object (assuming date is in date format)
            date_base = self.date if isinstance(self.date, datetime) else datetime.combine(self.date, datetime.min.time())

            # Set from_date and to_date based on 'date' and time inputs
            self.from_date = date_base.replace(hour=from_hours, minute=from_minutes, second=0)
            self.to_date = date_base.replace(hour=to_hours, minute=to_minutes, second=0)

            # Ensure the time range is valid
            if self.to_date < self.from_date:
                raise ValidationError(_("The 'To Time' must be greater than or equal to the 'From Time'."))

            # Calculate and assign the rounded duration
            self.unit_amount = self._compute_rounded_duration(self.from_date, self.to_date)

    @api.constrains('unit_amount', 'from_date', 'to_date')
    def _check_duration(self):
        """ Ensure that the duration matches the rounded time difference between from_date and to_date """
        for record in self:
            if record.from_date and record.to_date:
                expected_duration = self._compute_rounded_duration(record.from_date, record.to_date)
                if expected_duration != record.unit_amount:
                    raise ValidationError(_("The duration (unit_amount) does not match the time difference between 'From Date' and 'To Date'."))