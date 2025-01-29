from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class TeamTaskActivity(models.Model):
    _name = 'team.task.activity'
    _description = 'Team Task Activity'

    task_id = fields.Many2one('project.task', string="Task", required=True, ondelete="cascade")
    from_date = fields.Char("From Time (hh:mm)")
    to_date = fields.Char("To Time (hh:mm)")
    description = fields.Char("Activity Description")

    @api.constrains('from_date', 'to_date')
    def _check_time_format_and_logic(self):
        """ Validare pentru formatul și logica orelor din from_date și to_date """
        time_pattern = re.compile(r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]$')  # Format hh:mm

        for record in self:
            # Validare format 'hh:mm' pentru from_date și to_date
            if record.from_date and not time_pattern.match(record.from_date):
                raise ValidationError(_("The 'From Time' must be in the format 'hh:mm' and within 00:00 to 23:59."))

            if record.to_date and not time_pattern.match(record.to_date):
                raise ValidationError(_("The 'To Time' must be in the format 'hh:mm' and within 00:00 to 23:59."))

            # Conversia la ore și minute pentru validarea logică
            if record.from_date and record.to_date:
                from_hours, from_minutes = map(int, record.from_date.split(':'))
                to_hours, to_minutes = map(int, record.to_date.split(':'))

                # Verifică dacă `to_date` este ulterior față de `from_date`
                if (to_hours, to_minutes) <= (from_hours, from_minutes):
                    raise ValidationError(_("The 'To Time' must be later than 'From Time'."))