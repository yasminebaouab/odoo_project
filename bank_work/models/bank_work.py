# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BankWork(models.Model):
    _name = 'bank.work'

    def _check_admin(self):
        """ Checks if user is responsible for this request
        @return: Dictionary of values
        """
        res = {}
        user = self.env['res.users'].browse(self.env.user.id)
        for req in self:
            if user.id == 1:
                res[req.id] = True
            else:
                res[req.id] = False

        return res

    name = fields.Char(string='Work summary')
    ftp = fields.Char(string='ftp', readonly=True)
    date = fields.Datetime(string='Date', select="1")
    date_r = fields.Datetime('Date', select="1")
    is_admin = fields.Boolean(compute='_check_admin', string='Admin ?')
    bon_id = fields.Many2one('bon.show', string='Event')
    date_start = fields.Date(string='Date', select="1")
    date_end = fields.Date(string='Date', select="1")
    employee_id = fields.Many2one('hr.employee', string='Task')
    project_id = fields.Many2one('project.project', string='Project', ondelete='set null', select=True,
                                 track_visibility='onchange', change_default=True)
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade', select="1")
    product_id = fields.Many2one('product.product', string='Task', ondelete='cascade', select="1")
    partner_id = fields.Many2one('res.partner', string='Superviseur')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('valid', 'Validé'), ],
        string='Status', copy=False, default='draft')
    categ_id = fields.Many2one('product.category', string='Tags')
    note = fields.Text(string='Work summary')
    wage = fields.Float(string='T.H')
    amnt = fields.Float(string='T.H')
    wage_ch = fields.Float(string='T.H')
    amnt_ch = fields.Float(string='T.H')

    @api.onchange('wage_ch', 'employee_id')
    def onchange_wage(self):
        vals = {}
        emp = self.env['hr.employee'].browse(self.employee_id.id)
        if self.wage_ch:
            vals.update({'amnt_ch': self.wage_ch * emp.contract_id.wage})

        return {'value': vals}

    # def onchange_date_to_(self, cr, uid, ids, date_to, date_from, employee_id, task_id, context=None):
    #     """
    #     Update the number_of_days.
    #     """
    #
    #     # date_to has to be greater than date_from
    #     result = {'value': {}}
    #     if (date_from and date_to):
    #         if (date_from and date_to) and (date_from > date_to):
    #             raise osv.except_osv(_('Warning!'), _('The start date must be anterior to the end date.'))
    #
    #         result = {'value': {}}
    #         ## if ids:
    #         this = self.pool.get('project.task').browse(cr, uid, task_id, context=context)
    #
    #         ##for work in self.browse(cr, uid, ids):
    #         employee_obj = self.pool.get('hr.employee')
    #         academic_obj = self.pool.get('hr.academic')
    #         empl = employee_obj.browse(cr, uid, employee_id, context=context)
    #         holiday_obj = self.pool.get('hr.holidays')
    #         hours_obj = self.pool.get('training.holiday.year')
    #         rate_obj = self.pool.get('res.users.role')
    #
    #         ##        rate_obj.search(cr, uid, [('employee_ids.','=', str(date_from[:4]))])
    #         # Compute and update the number of days
    #         wage = empl.contract_id.wage
    #         if (date_to and date_from) and (date_from <= date_to):  ##'%Y-%m-%d %H:%M:%S'
    #             DATETIME_FORMAT = "%Y-%m-%d"
    #             from_dt = dt.datetime.strptime(date_from, DATETIME_FORMAT)
    #             to_dt = dt.datetime.strptime(date_to, DATETIME_FORMAT)
    #             timedelta = to_dt - from_dt
    #             diff_day = holiday_obj._get_number_of_days(cr, uid, date_from, date_to)
    #             ##diff_day = timedelta.days
    #             year = hours_obj.search(cr, uid, [('year', '=', str(date_from[:4]))])
    #             if year:
    #                 hr = hours_obj.browse(cr, uid, year[0], context=context).hours
    #             else:
    #                 hr = 7
    #             ##  raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%year)
    #             result['value']['color1'] = round(math.floor(diff_day)) + 1
    #             result['value']['hours_r'] = (round(math.floor(diff_day)) + 1) * hr
    #         ##  result['value']['total_r'] = ((round(math.floor(diff_day))+1))*hr *wage
    #         ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%work)
    #
    #         else:
    #
    #             result['value']['color1'] = 0
    #             result['value']['total_r'] = 0
    #
    #     return result
    #
    # def action_open_group(self, cr, uid, ids, context=None):
    #     current = self.browse(cr, uid, ids[0], context=context)
    #     work_line = self.pool.get('project.task.work.line')
    #     tt = []
    #
    #     if work_line.browse(cr, uid, current.id, context).group_id2:
    #         tt.append(work_line.browse(cr, uid, current.id, context).group_id2.id)
    #         return {
    #             'name': ('Consultation Bon Source'),
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             ##'views':[[1544,'tree']],
    #             'target': 'popup',
    #             'res_model': 'base.group.merge.automatic.wizard',
    #             ##  'res_id': current.paylist_id.id,
    #             'res_id': tt[0],
    #             'context': {},
    #             'domain': [('id', 'in', tt)]
    #         }
    #
    def confirm(self):
        this = self[0]
        if this.wage_ch == 0:
            raise UserError(_('Erreur!\nNbres d"heures doit etres superieur à 0!'))
        nb = this.employee_id.bank_hours + this.wage_ch
        self.write({'state': 'valid'})
        self.env['hr.employee'].browse(this.employee_id.id).write({'bank_hours': nb})
        return True

    # def save(self, cr, uid, ids, context=None):
    #     this = self.browse(cr, uid, ids[0])
    #     if this.hours_ch == 0:
    #         raise osv.except_osv(_('Erreur!'), _('Nbres d"heures doit etres superieur à 0!'))
    #     ##'total_t'
    #     ##cr.execute('update project_task set remaining_hours=remaining_hours - %s + (%s) where id=%s', (vals.get('hours',0.0), work.hours, work.task_id.id))
    #
    #     self.write(cr, uid, ids, {'state': 'done'}, context=context)
    #     return True

    # def onchange_hours_(self, cr, uid, ids, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r,
    #                     context=None):
    #     """
    #     Update the number_of_days.
    #     """
    #
    #     employee_obj = self.pool.get('hr.employee')
    #     academic_obj = self.pool.get('hr.academic')
    #
    #     ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
    #     ##task_obj = self.pool.get('project.task.work')
    #     empl = employee_obj.browse(cr, uid, employee_id, context=context)
    #
    #     result = {'value': {}}
    #     ##this=self.browse(cr, uid, ids[0])
    #     ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%hours_r)
    #     ##result['value']['total_r'] = hours_r
    #     ##for work in self.browse(cr, uid, ids):
    #
    #     # Compute and update the number of days
    #
    #     ##if hours_r:
    #
    #     if hours_r:
    #         wage = 0
    #         aca = academic_obj.search(cr, uid, [('employee_id', '=', employee_id)])
    #         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%aca)
    #         if aca:
    #             for list in aca:
    #
    #                 if list:
    #                     ligne = academic_obj.browse(cr, uid, list, context=context)
    #                     if ligne.curr_ids:
    #                         for ll in ligne.curr_ids:
    #                             if ll.product_id and ll.uom_id:
    #                                 if (ll.product_id.id == product_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.product_id and ll.uom_id2:
    #                                     if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #
    #                             elif ll.product_id and ll.uom_id2:
    #                                 if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.categ_id and ll.uom_id2:
    #                                     if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id2:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             else:
    #                                 raise osv.except_osv(_('Errour!'),
    #                                                      _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                     else:
    #                         raise osv.except_osv(_('Errour!'),
    #                                              _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                 else:
    #                     raise osv.except_osv(_('Errour!'),
    #                                          _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         else:
    #             raise osv.except_osv(_('Errour!'),
    #                                  _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #
    #         if wage == 0:
    #             raise osv.except_osv(_('Errour!'),
    #                                  _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         if uom_id == 5:
    #             result['value']['total_r'] = hours_r * wage
    #         else:
    #             result['value']['total_r'] = poteau_r * wage
    #     return result
    #
    # def onchange_qty_(self, cr, uid, ids, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r, date_to,
    #                   date_from, task_id, context=None):
    #     """
    #     Update the number_of_days.
    #     """
    #
    #     employee_obj = self.pool.get('hr.employee')
    #     academic_obj = self.pool.get('hr.academic')
    #
    #     ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
    #     ##task_obj = self.pool.get('project.task.work')
    #     empl = employee_obj.browse(cr, uid, employee_id, context=context)
    #
    #     result = {'value': {}}
    #     ##this=self.browse(cr, uid, ids[0])
    #     ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%hours_r)
    #     ##result['value']['total_r'] = hours_r
    #     ##for work in self.browse(cr, uid, ids):
    #
    #     # Compute and update the number of days
    #
    #     ##if hours_r:
    #
    #     if poteau_r:
    #         wage = 0
    #         aca = academic_obj.search(cr, uid, [('employee_id', '=', employee_id)])
    #         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%aca)
    #         if aca:
    #             for list in aca:
    #
    #                 if list:
    #                     ligne = academic_obj.browse(cr, uid, list, context=context)
    #                     if ligne.curr_ids:
    #                         for ll in ligne.curr_ids:
    #                             if ll.product_id and ll.uom_id:
    #                                 if (ll.product_id.id == product_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.product_id and ll.uom_id2:
    #                                     if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #
    #                             elif ll.product_id and ll.uom_id2:
    #                                 if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.categ_id and ll.uom_id2:
    #                                     if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id2:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             else:
    #                                 raise osv.except_osv(_('Errour!'),
    #                                                      _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                     else:
    #                         raise osv.except_osv(_('Errour!'),
    #                                              _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                 else:
    #                     raise osv.except_osv(_('Errour!'),
    #                                          _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         else:
    #             raise osv.except_osv(_('Errour!'),
    #                                  _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #
    #         if wage == 0:
    #             raise osv.except_osv(_('Errour!'),
    #                                  _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         if uom_id == 5:
    #             result['value']['total_r'] = hours_r * wage
    #         else:
    #             result['value']['total_r'] = poteau_r * wage
    #         self.onchange_date_to_(cr, uid, ids, date_to, date_from, employee_id, task_id, context)
    #     return result
    #
    # def onchange_uom_id_(self, cr, uid, ids, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r, date_to,
    #                      date_from, task_id, context=None):
    #     """
    #     Update the number_of_days.
    #     """
    #
    #     employee_obj = self.pool.get('hr.employee')
    #     academic_obj = self.pool.get('hr.academic')
    #
    #     ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
    #     ##task_obj = self.pool.get('project.task.work')
    #     empl = employee_obj.browse(cr, uid, employee_id, context=context)
    #
    #     result = {'value': {}}
    #     ##this=self.browse(cr, uid, ids[0])
    #     ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%hours_r)
    #     ##result['value']['total_r'] = hours_r
    #     ##for work in self.browse(cr, uid, ids):
    #
    #     # Compute and update the number of days
    #
    #     ##if hours_r:
    #
    #     if uom_id:
    #         wage = 0
    #         aca = academic_obj.search(cr, uid, [('employee_id', '=', employee_id)])
    #         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%aca)
    #         if aca:
    #             for list in aca:
    #
    #                 if list:
    #                     ligne = academic_obj.browse(cr, uid, list, context=context)
    #                     if ligne.curr_ids:
    #                         for ll in ligne.curr_ids:
    #                             if ll.product_id and ll.uom_id:
    #                                 if (ll.product_id.id == product_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.product_id and ll.uom_id2:
    #                                     if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #
    #                             elif ll.product_id and ll.uom_id2:
    #                                 if (ll.product_id.id == product_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id.id == uom_id):
    #                                     wage = ll.amount
    #                                 elif ll.categ_id and ll.uom_id2:
    #                                     if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                         wage = ll.amount2
    #
    #                             elif ll.categ_id and ll.uom_id2:
    #                                 if (ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id):
    #                                     wage = ll.amount2
    #
    #                             else:
    #                                 raise osv.except_osv(_('Errour!'),
    #                                                      _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                     else:
    #                         raise osv.except_osv(_('Errour!'),
    #                                              _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #                 else:
    #                     raise osv.except_osv(_('Errour!'),
    #                                          _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         else:
    #             raise osv.except_osv(_('Errour!'),
    #                                  _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #
    #         ##                if wage==0:
    #         ##                    raise osv.except_osv(_('Errour!'),
    #         ##                                         _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
    #         if uom_id == 5:
    #             result['value']['total_r'] = hours_r * wage
    #         else:
    #             result['value']['total_r'] = poteau_r * wage
    #         self.onchange_date_to_(cr, uid, ids, date_to, date_from, employee_id, task_id, context)
    #     return result
    #
    # def action_invoice(self, cr, uid, ids, context=None):
    #     project_ids = ids[0]
    #     current = self.browse(cr, uid, ids[0], context=context)
    #
    #     if current.group_id:
    #         if current.group_id.type == 'Feuille de Temps':
    #             return {
    #                 'name': ('Feuille de Temps'),
    #                 'type': 'ir.actions.act_window',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'target': 'new',
    #                 'res_model': 'bon.show',
    #                 'res_id': current.group_id.id,
    #                 'view_id': 1622,
    #                 'context': {},
    #                 'domain': []
    #             }
    #         else:
    #             return {
    #                 'name': ('Facture'),
    #                 'type': 'ir.actions.act_window',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'target': 'new',
    #                 'res_model': 'bon.show',
    #                 'res_id': current.group_id.id,
    #                 'view_id': 1727,
    #                 'context': {},
    #                 'domain': []
    #             }
    #
    # def button_confirm(self, cr, uid, ids, context=None):
    #
    #     this = self.browse(cr, uid, ids[0])
    #     if this.poteau_r <= 0:
    #         raise osv.except_osv(_('Erreur!'), _('Qté Réalisée doit etre déclarée!'))
    #     ##'total_t'
    #     ##cr.execute('update project_task set remaining_hours=remaining_hours - %s + (%s) where id=%s', (vals.get('hours',0.0), work.hours, work.task_id.id))
    #
    #     self.write(cr, uid, ids, {'state': 'done'}, context=context)
    #     return True
    #
    # def button_save_(self, cr, uid, ids, context=None):
    #
    #     this = self.browse(cr, uid, ids[0])
    #
    #     raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.') % ids[0])
    #     ##self.write(cr, uid, ids, {'note': 'note' }, context=context)
    #
    #     return {
    #         'name': ('Modification Travaux'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'res_model': 'project.task.work',
    #         'res_id': ids[0],
    #         'context': {},
    #         'domain': []
    #     }
    #
    # def action_file(self, cr, uid, ids, context=None):
    #     project_ids = ids[0]
    #     current = self.browse(cr, uid, ids[0], context=context)
    #
    #     if current.wizard_id:
    #         return {
    #             'name': ('Bons A Valider'),
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'new',
    #             'res_model': 'base.invoice.merge.automatic.wizard',
    #             'res_id': current.wizard_id.id,
    #             'context': {},
    #             'domain': []
    #         }
    #
    # def open_invoice_cust(self, cr, uid, ids, context=None):
    #     project_ids = ids[0]
    #     current = self.browse(cr, uid, ids[0], context=context)
    #
    #     if current.num:
    #         num = self.pool.get('base.facture.wizard').search(cr, uid, [('num', '=', current.num)])
    #         if num:
    #             this_id = num[0]
    #             return {
    #                 'name': ('Factures Clients'),
    #                 'type': 'ir.actions.act_window',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'target': 'new',
    #                 'res_model': 'base.facture.wizard',
    #                 'res_id': this_id,
    #                 'context': {},
    #                 'domain': []
    #             }
    #
    # ##    def action_cancel(self, cr, uid, ids, context=None):
    # ##        alias_ids = []
    # ##
    # ##        for proj in self.browse(cr, uid, ids, context=context):
    # ##            if proj.paylist_id or proj.wizard_id:
    # ##                raise osv.except_osv(_('Action Invalide!'),
    # ##                                     _('Impossible de supprimer une ligne validée ou facturée!'))
    # ##            cr.execute("delete from  project_task_work_line WHERE id = %s", (proj.id,))
    # ##            return {
    # ##            'name'          :   ('Modification Travaux'),
    # ##            'type'          :   'ir.actions.act_window',
    # ##            'view_type'     :   'form',
    # ##            'view_mode'     :   'form',
    # ##            'target'        :   'new',
    # ##            'res_model'     :   'project.task.work',
    # ##            'res_id': proj.work_id.id,
    # ##            'context': {},
    # ##            'domain'        :   []
    # ##            }
    # def action_delete(self, cr, uid, ids, context=None):
    #     project_ids = ids[0]
    #     current = self.browse(cr, uid, ids[0], context=context)
    #     parent = current.work_id.id
    #     if current.paylist_id or current.wizard_id:
    #         raise osv.except_osv(_('Action Invalide!'),
    #                              _('Impossible de supprimer une ligne validée ou facturée!'))
    #
    #     ##cr.execute("delete from  project_task_work_line WHERE id = %s", (proj.id,))
    #     ## proj.unlink(cr, uid, proj.id, context=context)
    #     self.pool.get('project.task.work.line').unlink(cr, uid, current.id, context=context)
    #     ##if current.wizard_id:
    #     return {
    #         'name': ('Bons A Valider'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'res_model': 'project.task.work',
    #         'res_id': parent,
    #         'context': {},
    #         'domain': []
    #     }
    #
    # def action_cancel(self, cr, uid, ids, context=None):
    #     alias_ids = []
    #     current = self.browse(cr, uid, ids[0], context=context)
    #
    #     for proj in self.browse(cr, uid, ids, context=context):
    #         if proj.paylist_id or proj.wizard_id:
    #             raise osv.except_osv(_('Action Invalide!'),
    #                                  _('Impossible de supprimer une ligne validée ou facturée!'))
    #
    #         ##cr.execute("delete from  project_task_work_line WHERE id = %s", (proj.id,))
    #     ## proj.unlink(cr, uid, proj.id, context=context)
    #     self.pool.get('project.task.work.line').unlink(cr, uid, current.id, context=context)
    #     return
    #     {
    #         'name': ('Modification Travaux'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #
    #         'res_model': 'project.task.work',
    #         'res_id': current.work_id.id,
    #         'context': {},
    #         'domain': []
    #     }
    #
    #
    #
