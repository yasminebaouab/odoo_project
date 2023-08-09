from odoo import models, fields, api
from datetime import datetime as dt
from odoo.exceptions import UserError
from odoo.tools.translate import _
import math


class IntervenantsAffectProduction(models.Model):
    _name = 'intervenants.affect.production'
    _description = 'intervenants affectés à la production'
    _rec_name = 'id'

    # Chaque classe a une relation many2one avec project_task_work et permet de stocker
    # l'id de l'employé, son nom, le statut (non traité, ou traité), date affectation, et date D.B.

    name = fields.Char('name')
    employee_id = fields.Integer('Employee')
    state = fields.Char('Status')
    date_affectation = fields.Date('Date affectation')
    date_declaration_bon = fields.Date('Date Declaration')
    task_work_id = fields.Many2one('project.task.work', 'Task Work')