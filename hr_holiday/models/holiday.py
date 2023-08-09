# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta
import math


class HrHolidaysStatus(models.Model):
    _name = "hr.holidays.type"
    _description = "Leave Type"
    _rec_name = "name"

    name = fields.Char(string='Type de Congé', size=64, required=True, translate=True,
                       readonly=True, states={'draft': [('readonly', False)]})
    categ_id = fields.Many2one('calendar.event.type', string='Type de Réunion',
                               readonly=True, states={'draft': [('readonly', False)]})
    color_name = fields.Selection([('red', 'Red'),
                                   ('blue', 'Blue'),
                                   ('lightgreen', 'Light Green'),
                                   ('lightblue', 'Light Blue'),
                                   ('lightyellow', 'Light Yellow'),
                                   ('magenta', 'Magenta'),
                                   ('lightcyan', 'Light Cyan'),
                                   ('black', 'Black'),
                                   ('lightpink', 'Light Pink'),
                                   ('brown', 'Brown'),
                                   ('violet', 'Violet'),
                                   ('lightcoral', 'Light Coral'),
                                   ('lightsalmon', 'Light Salmon'),
                                   ('lavender', 'Lavender'),
                                   ('wheat', 'Wheat'),
                                   ('ivory', 'Ivory')], default='red', required=True,
                                  string='Couleur Affichée dans le Rapport',
                                  readonly=True, states={'draft': [('readonly', False)]})
    limit = fields.Boolean(string='Autoriser de Dépasser La Limite de Jours', default=False)
    active = fields.Boolean(string='Active', default=True)
    max_leave = fields.Integer(string='Nombre de Jours Maximal', required=True,
                               readonly=True, states={'draft': [('readonly', False)]})
    employee_ids = fields.Many2many('hr.employee', string='Employés Concernés',
                                    readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Brouillon'), ('valid', 'Validé')],
        string='Status', readonly=True, copy=False, default='draft')

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'Le Type de Congé doit être unique !'),
    ]

    def unlink(self):
        for rec in self:
            if rec.state == 'valid':
                raise UserError(
                    _('Action Impossible !\nImpossible de supprimer un type de Congé validé !'))

        return super(HrHolidaysStatus, self).unlink()

    def inject(self):

        if self.employee_ids:
            emp_ids = self.employee_ids.ids
        else:
            emp_ids = self.env['hr.employee'].search([]).ids

        emp_hol = self.env['hr.employee.holiday']
        for tt in emp_ids:
            emp_hol.create({
                'name': self.name,
                'employee_id': tt,
                'max_leave': self.max_leave,
                'remaining_leave': self.max_leave,
                'limit': self.limit,
            })

        self.state = 'valid'

        view = self.env['sh.message.wizard']
        view_id = view and view.id or False
        return {
            'name': 'Type ajouté avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }

    def cancel(self):
        self.state = 'draft'
        if self.employee_ids:
            emp_ids = self.employee_ids.ids
        else:
            emp_ids = self.env['hr.employee'].search([]).ids

        emp_hol = self.env['hr.employee.holiday']
        for tt in emp_ids:
            emp_hol.search([('employee_id', '=', tt), ('name', '=', self.name)]).unlink()
        view = self.env['sh.message.wizard']
        view_id = view and view.id or False
        return {
            'name': 'Type supprimé avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }


# if record.gest_id.user_id.id == self._uid:


class HrHolidays(models.Model):
    _name = 'hr.holidays'
    _description = "Leave"
    _order = 'date desc'

    def name_get(self):
        res = []
        for rec in self:
            name = str(rec.date) + ' - ' + str(rec.holiday_type_id.name)
            res.append((rec.id, name))
        return res

    def _employee_get(self):
        emp_id = self._context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).ids
        if emp_ids:
            return emp_ids[0]
        return False

    name = fields.Char(string='Référence')
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('pending', 'En cours de Traitement'),
            ('accept', 'Accepté'),
            ('refuse', 'Refusé'),
            ('modify', 'Modifié')],
        string='Status', readonly=True, copy=False, default='draft')
    date = fields.Date(string='Date de demande', default=fields.date.today())
    date_from = fields.Date(string='Date de Début', readonly=True, required=True,
                            states={'draft': [('readonly', False)]}, copy=False)
    date_to = fields.Date(string='Date de Fin', readonly=True, required=True,
                          states={'draft': [('readonly', False)]}, copy=False)
    date_from_r = fields.Date(string='Nouvelle Date de Début', readonly=True, required=True,
                              states={'draft': [('readonly', False)]}, copy=False)
    date_to_r = fields.Date(string='Nouvelle Date de Fin', readonly=True, required=True,
                            states={'draft': [('readonly', False)]}, copy=False)
    employee_id = fields.Many2one('hr.employee', string='Employé', select=True, invisible=False,
                                  readonly=True, default=lambda self: self._employee_get(), )
    manager_id = fields.Many2one('hr.employee', 'Superviseur', invisible=False, readonly=True,
                                 states={'draft': [('readonly', False)]}, copy=False, required=True,
                                 help='This area is automatically filled by the user who validate the leave')
    notes = fields.Text(string='Reasons', readonly=True,
                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    notes_r = fields.Text(string='Reasons', readonly=True,
                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    number_of_days = fields.Float(string='Nombre de Jours', copy=False)
    number_of_days_r = fields.Float(string='Nouveau Nombre de Jours')
    meeting_id = fields.Many2one('calendar.event', string='Meeting')
    user_id = fields.Many2one('res.users', string='Utilisateur')
    holiday_line_ids = fields.One2many('hr.holidays.line', 'holiday_id')
    holiday_type_id = fields.Many2one('hr.holidays.type', string='Type de Congé', required=True,
                                      readonly=True, states={'draft': [('readonly', False)]})
    holiday_id = fields.Many2one('hr.holidays', string='Congé')
    type = fields.Selection([('take', 'Demande Congé'), ('modify', 'Modification Congé')],
                            string='Type Opération')

    _sql_constraints = [
        ('type_value',
         "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or (holiday_type='category' AND category_id IS NOT NULL))",
         "The employee or employee category of this request is missing. Please make sure that your user login is linked to an employee."),
        ('date_check2', "CHECK ( (type='add') OR (date_from <= date_to))",
         "The start date must be anterior to the end date."),
        ('date_check', "CHECK ( number_of_days >= 0 )", "The number of days must be greater than 0."),
    ]

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'pending'):
                raise UserError(
                    _('Action Impossible !\nImpossible de Supprimer une Demande Traitée !'))

        return super(HrHolidays, self).unlink()

        # TODO: can be improved using resource calendar method

    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""
        holiday_proxy = self.env['training.holiday.year']
        if not holiday_proxy.search([('year', '=', date.today().year)]):
            return False
        i = 0
        while date_from < date_to:
            dayoff = self.env['training.holiday.period'].search([('date_start', '<=', date_from),
                                                                 ('date_stop', '>=', date_from)])
            if dayoff:
                i += 1
            date_from = date_from + relativedelta(days=1)
        timedelta = date_to - date_from
        diff_day = timedelta.days
        diff_day -= i
        return i

    @api.onchange('date_to', 'date_from')
    def onchange_date_from(self):
        """
        If there are no date set for date_to, automatically set one 8 hours later than
        the date_from.
        Also update the number_of_days.
        """
        date_from = self.date_from
        date_to = self.date_to
        # date_to has to be greater than date_from
        if (date_from and date_to) and (date_from > date_to):
            raise UserError(_('Attention!\nLa date de début doit être antérieur à la date de fin.'))

        result = {'value': {}}
        holy = self.env['hr.public.holiday'].search([('date_from', '>=', date_from), ('date_to', '<=', date_to),
                                                     ('state', '=', 'validate')]).ids
        cpt = 0
        if holy:
            for jj in holy:
                hh = self.env['hr.public.holiday'].browse(jj)
                cpt = cpt + hh.nbr

        # No date_to set so far: automatically compute one 8 hours later

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            timedelta = date_to - date_from
            diff_day = timedelta.days
            diff_day1 = self._get_number_of_days(date_from, date_to)
            if diff_day1 == 0:
                diff_day = diff_day + 1
            self.number_of_days = diff_day - diff_day1 - cpt
        else:
            self.number_of_days = 0

        self.number_of_days_r = self.number_of_days
        self.date_from_r = self.date_from
        self.date_to_r = self.date_to

        return result

    @api.onchange('employee_id')
    def onchange_employee(self):
        type_ids = []
        emp_hol_ids = self.env['hr.employee.holiday'].search([('employee_id', '=', self.employee_id.id)]).ids
        hol_line = self.env['hr.holidays.line']
        for tt in emp_hol_ids:
            emp_hol = self.env['hr.employee.holiday'].browse(tt)
            type_ids.append(emp_hol.name)
            hol_line.create({
                'holiday_id': self.id,
                'name': emp_hol.name,
                'max_leave': emp_hol.max_leave,
                'remaining_leave': emp_hol.remaining_leave,
                'limit': emp_hol.limit,
            })
        return {'domain': {'holiday_type_id': [('name', 'in', type_ids)]}}

    def button_send(self):
        name = self.env['hr.holidays.type'].browse(self.holiday_type_id.id).name
        sol_id = self.env['hr.employee.holiday'].search(
            [('name', '=', name), ('employee_id', '=', self.employee_id.id)]).id
        sol = self.env['hr.employee.holiday'].browse(sol_id).remaining_leave
        nb_days = self.number_of_days
        if nb_days > sol:
            raise UserError('Solde Insuffisant')
        else:
            self.write({'state': 'pending'})

    def button_reopen(self):
        self.write({'state': 'draft'})

    def button_accept(self):
        name = self.env['hr.holidays.type'].browse(self.holiday_type_id.id).name
        sol_id = self.env['hr.employee.holiday'].search(
            [('name', '=', name), ('employee_id', '=', self.employee_id.id)]).id
        sol = self.env['hr.employee.holiday'].browse(sol_id).remaining_leave
        nb_days = self.number_of_days
        self.env['hr.employee.holiday'].browse(sol_id).write({'remaining_leave': sol - nb_days})

        self.env['hr.holidays.histo'].create({
            'holiday_id': self.id,
            'employee_id': self.employee_id.id,
            'date': self.date,
            'diff': nb_days,
            'year': self.date.year(),
        })

        self.write({'state': 'accept'})

    def button_refuse(self):
        self.write({'state': 'refuse'})


class HrHolidayLine(models.Model):
    _name = 'hr.holidays.line'

    holiday_id = fields.Many2one('hr.holidays', string='Congé')
    name = fields.Char(string='Type de Congé', size=64, translate=True)
    max_leave = fields.Integer(string='Nombre de Jours Maximal')
    remaining_leave = fields.Integer(string='Nombre de Jours Restant')
    limit = fields.Boolean(string='Autoriser de Dépasser La Limite de Jours')


class HrHolidayHisto(models.Model):
    _name = 'hr.holidays.histo'

    holiday_id = fields.Many2one('hr.holidays', string='Référence Congé')
    employee_id = fields.Many2one('hr.employee', string='Employé')
    date = fields.Date(string='Date Opération')
    diff = fields.Float(string='Nombre de Jours')
    year = fields.Integer(string='Année fiscale')
