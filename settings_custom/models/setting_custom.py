from odoo import models, fields, api


class SettingsCustom(models.Model):
    _name = 'settings.custom'
    _description = ''
    _rec_name = "name"

    name = fields.Char(string="Settings custom", required=True, translate=True, default='Settings custom')

    affectation_multiple = fields.Selection([
        ('0', 'Affectation Multiple'),
        ('1', 'Affectation Simple'),
    ], string="Type d'affectation")
    _sql_constraints = [
        ('unique_settings_custom', 'UNIQUE(name)', 'Only one record allowed in Settings Custom table!')
    ]

    @api.model
    def default_get(self, fields_list):
        defaults = super(SettingsCustom, self).default_get(fields_list)
        existing_record = self.search([], limit=1)
        if existing_record:
            defaults['affectation_multiple'] = existing_record.affectation_multiple
        return defaults
    @api.model
    def create(self, vals):
        existing_record = self.search([], limit=1)
        if existing_record:
            existing_record.write(vals)
            return existing_record
        else:
            return super(SettingsCustom, self).create(vals)

# if not affectation_multiple and work.state == 'draft':
#     print('affectation_simple:', 'draft')
#
#     if 'correction' in work.product_id.name or u'Contrôle' in work.product_id.name:
#         print('correction:', 'Contrôle')
#
#         vv = []
#         if work.kit_id:
#             kit_list = self.env['project.task.work'].search([
#                 ('id', 'in', active_ids),
#             ])
#             print('*****kit_list******:', kit_list)
#
#             for kit_work in kit_list:
#                 if not work.is_copy and not kit_work.is_copy:
#                     vv.append(kit_work.id)
#                 elif kit_work.is_copy and work.rank == kit_work.rank:
#                     vv.append(kit_work.id)
#             print('vv', vv)
#             res['work_ids'] = vv
#             print('res 0:', res)
#             print('active_ids :', active_ids)

