from odoo import models, fields


class SettingsCustom(models.Model):
    _name = 'settings.custom'
    _description = ''

    affectation_multiple = fields.Boolean(string="Type d'affectation")


