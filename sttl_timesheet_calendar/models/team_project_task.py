from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

class TeamProjectTask(models.Model):
    _inherit = 'project.task'

    team_activity_ids = fields.One2many('team.task.activity', 'task_id', string="Team Activities")

    material_ids = fields.One2many('task.material', 'task_id', string="Materials")
    transport_ids = fields.One2many('task.transport', 'task_id', string="Transport")

    def action_generate_timesheets(self):
        """
        Generate timesheets for tasks, logging all events and errors for debugging.
        """
    
        success_count = 0
        error_count = 0
        error_log = []

        logging.info("Starting timesheet generation process.")

        for task in self:
            try:
                logging.info(f"Processing task: {task.name} (ID: {task.id})")

                # Șterge atașările anterioare
                existing_lines = self.env['account.analytic.line'].search([('task_id', '=', task.id)])
                if existing_lines:
                    logging.info(f"Deleting existing timesheets for task '{task.name}' (ID: {task.id}).")
                    existing_lines.unlink()

                if not task.date_deadline:
                    error_message = f"Task '{task.name}' skipped: no deadline set."
                    logging.warning(error_message)
                    error_log.append(error_message)
                    continue

                employees = task.user_ids.filtered(lambda u: u.employee_id).mapped('employee_id')
                if not employees:
                    error_message = f"Task '{task.name}' skipped: no employees associated."
                    logging.warning(error_message)
                    error_log.append(error_message)
                    continue

                for activity in task.team_activity_ids:
                    try:
                        logging.info(f"Processing activity: {activity.description} (from_date: {activity.from_date}, to_date: {activity.to_date})")

                        # Validate and parse time fields
                        from_hours, from_minutes = map(int, activity.from_date.split(':'))
                        to_hours, to_minutes = map(int, activity.to_date.split(':'))

                        if not (0 <= from_hours < 24 and 0 <= from_minutes < 60 and
                                0 <= to_hours < 24 and 0 <= to_minutes < 60):
                            raise ValueError("Invalid time format")

                        # Calculate datetime objects
                        date_base = datetime.combine(task.date_deadline, datetime.min.time())
                        from_datetime = date_base.replace(hour=from_hours, minute=from_minutes)
                        to_datetime = date_base.replace(hour=to_hours, minute=to_minutes)

                        # Check duration validity
                        calculated_duration = (to_datetime - from_datetime).total_seconds() / 3600
                        if calculated_duration <= 0:
                            raise ValueError(f"Invalid duration: {calculated_duration} hours. 'From' time must be before 'To' time.")

                        # Iterate over all employees and create timesheets
                        for employee in employees:
                            logging.info(f"Creating timesheet for employee '{employee.name}' in task '{task.name}' (Activity: '{activity.description}').")
                            self.env['account.analytic.line'].create({
                                'name': activity.description,
                                'employee_id': employee.id,
                                'date': task.date_deadline,
                                'from_time': activity.from_date,
                                'to_time': activity.to_date,
                                'from_date': from_datetime,
                                'to_date': to_datetime,
                                'unit_amount': calculated_duration,
                                'project_id': task.project_id.id,
                                'task_id': task.id,
                            })
                            success_count += 1

                    except ValueError as e:
                        error_message = f"Activity '{activity.description}' in task '{task.name}' skipped: {str(e)}"
                        logging.error(error_message)
                        error_log.append(error_message)
                        error_count += 1
                    except Exception as e:
                        error_message = f"Unexpected error for activity '{activity.description}' in task '{task.name}': {str(e)}"
                        logging.error(error_message)
                        error_log.append(error_message)
                        error_count += 1

            except Exception as e:
                error_message = f"Unexpected error for task '{task.name}': {str(e)}"
                logging.error(error_message)
                error_log.append(error_message)
                error_count += 1

        # Log summary
        logging.info(f"Timesheet generation process completed: {success_count} successes, {error_count} errors.")
        if error_log:
            for error in error_log:
                logging.error(error)

        # Notify user about the results
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Timesheet Generation Complete',
                'message': f"Successfully processed {success_count} entries. Encountered {error_count} errors.",
                'type': 'warning' if error_log else 'success',
                'sticky': True,  # Notification stays visible
            },
        }
