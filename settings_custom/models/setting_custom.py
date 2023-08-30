from odoo import models, fields


class SettingsCustom(models.Model):
    _name = 'settings.custom'
    _description = ''
    _rec_name = "name"

    # affectation_multiple = fields.Boolean()
    name = fields.Char(string="Settings custom", required=True, translate=True, default='Settings custom')

    affectation_multiple = fields.Selection([
        ('0', 'Affectation Multiple'),
        ('1', 'Affectation Simple'),
    ], string="Type d'affectation", default='0')


