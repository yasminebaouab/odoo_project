# -*- coding: utf-8 -*-
from datetime import date, timedelta
from multiprocessing import connection

from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
from odoo.tools.safe_eval import time, datetime


class MergeTasksLine(models.Model):
    _name = 'base.task.merge.line'
    _description = 'base_task_merge_line'

    min_id = fields.Integer(string='MinID', order='min_id asc')
    aggr_ids = fields.Char('Ids')
    zone = fields.Integer(string="Zone")
    zo = fields.Char(string="Zone")
    secteur = fields.Integer(string="Secteur")
    secteur_to = fields.Integer(string="Secteur")
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    poteau_t = fields.Float('Time Spent')
    is_display = fields.Boolean(string='Ids')
    plans = fields.Char(string='Ids')
    from_int = fields.Integer(string='MinID')
    to_int = fields.Integer(string='MinID')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    wizard_id = fields.Many2one('base.task.merge.automatic.wizard', string='Wizard')
    plan_id = fields.Many2one('risk.management.response.category', string='Wizard')
    plan_id2 = fields.Many2one('risk.management.response.category', string='Wizard')
    risk_id = fields.Many2one('risk.management.category', string='Wizard')

    def onchange_plan_id_(self, plan_id, plan_id2):
        result = {'value': {}}  # Initialisation d'un dictionnaire de résultats

        total = 0  # Initialisation d'une variable pour stocker le total des valeurs calculées

        if plan_id and plan_id2:  # Vérifie si les deux plan_id sont présents
            plan1 = self.env['risk.management.response.category'].browse(
                plan_id)  # Récupère l'enregistrement correspondant à plan_id dans le modèle 'risk.management.response.category'
            plan2 = self.env['risk.management.response.category'].browse(
                plan_id2)  # Récupère l'enregistrement correspondant à plan_id2 dans le modèle 'risk.management.response.category'

            # Parcours de la plage des identifiants de plan entre plan_id et plan_id2 inclus
            for x in range(plan_id, plan_id2 + 1):
                plan = self.env['risk.management.response.category'].browse(
                    x)  # Récupère chaque enregistrement correspondant à un identifiant de plan dans la plage
                if plan:
                    # Accumulation des valeurs des champs spécifiques de l'enregistrement plan dans la variable total
                    total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit

            # Assignation de la valeur calculée au champ 'plans' du dictionnaire de résultats
            result['value']['plans'] = plan1.plan + '-' + plan2.plan

        return result  # Retourne le dictionnaire de résultats contenant les valeurs mises à jour

    def onchange_plans(self, plans):
        result = {'value': {}}  # Initialisation d'un dictionnaire de résultats
        total = 0  # Initialisation d'une variable pour stocker le total des valeurs calculées
        count = 0  # Initialisation d'une variable pour compter

        if plans:  # Vérifie si le champ plans n'est pas vide
            if plans.count('-') > 1:  # Vérifie s'il y a plus d'un tiret dans plans
                raise ValidationError(_('Erreur !\nFormat Incorrecte!, un seul tiret est autorisé!'))
            elif plans.count('-') == 1 and plans.count(
                    ';') == 0:  # Vérifie s'il y a un seul tiret et aucun point-virgule dans plans
                tt = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[0])])
                tt1 = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[1])])
                if not tt:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t1 = tt[0]
                if not tt1:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t2 = tt1[0]
                for x in range(t1, t2):
                    plan = self.env['risk.management.response.category'].browse(x)
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            elif plans.count('-') == 1 and plans.count(
                    ';') > 0:  # Vérifie s'il y a un seul tiret et au moins un point-virgule dans plans
                tt = self.env['risk.management.response.category'].search(
                    [('plan', '=', (plans.split(';')[0]).split('-')[0])])
                tt1 = self.env['risk.management.response.category'].search(
                    [('plan', '=', (plans.split(';')[0]).split('-')[1])])
                if not tt:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t1 = tt[0]
                if not tt1:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t2 = tt1[0]
                for x in range(t1, t2):
                    plan = self.env['risk.management.response.category'].browse(x)
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
                    lst = (plans.split(';')[1]).split(';')
                    for kk in lst:
                        tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                        if not tt2:
                            raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                        else:
                            plan = self.env['risk.management.response.category'].browse(tt2[0])
                        if plan:
                            total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            elif plans.count('-') == 0 and plans.count(
                    ';') > 0:  # Vérifie s'il n'y a pas de tiret et au moins un point-virgule dans plans
                lst = plans.split(';')
                for kk in lst:
                    for kk in lst:
                        tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                        if not tt2:
                            raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                        else:
                            plan = self.env['risk.management.response.category'].browse(tt2[0])
                        if plan:
                            total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            else:
                raise ValidationError(
                    _('Erreur !\nFormat Incorrecte!, seuls les tirets "-" ou les points virgules ";" sont autorisés!'))

        result['value'][
            'poteau_t'] = total / 1000  # Calcule la valeur pour le champ 'poteau_t' dans le dictionnaire de résultats
        return result  # Retourne le dictionnaire de résultats contenant les valeurs mises à jour


class EbMergeTasks(models.Model):
    _name = 'base.task.merge.automatic.wizard'
    _description = 'Merge Tasks'
    _rec_name = 'name'

    """
            Action that shows the list of (non-draft) account moves from
            the selected journals and periods, so the user can review
            the renumbered account moves.
            """

    def show_results(self):

        """
        Action that shows the list of (non-draft) account moves from
        the selected journals and periods, so the user can review
        the renumbered account moves.
        """
        # Récupérer l'objet "current" qui est le premier enregistrement du modèle courant
        current = self[0]
        # Supprimer toutes les lignes associées à l'enregistrement "current" dans la table "base_group_merge_line2"
        self.env.cr.execute("delete from base_group_merge_line2 where wiz_id=%s", (current.id,))
        # Initialiser les listes "res_cpt" et "list"
        res_cpt = []
        list = []
        # Vérifier si un projet est sélectionné (current.project_id)
        if current.project_id:
            # Vérifier si le type de projet est égal à '1'
            if current.type == '1':
                # Vérifier si des tâches sont sélectionnées (current.task_ids)
                if not current.task_ids:
                    raise UserError(_('Action impossible!\nVous devez sélectionner les étapes/kits concernées!'))
                # Vérifier si des lignes sont présentes (current.line_ids)
                if not current.line_ids:
                    raise UserError(_('Action impossible!\nVous devez Mentionner les Zones et Secteurs!'))
                # Initialiser les listes "l" et "v"
                l = []
                v = []
                # Parcourir les tâches sélectionnées (current.task_ids.ids)
                for tt in current.task_ids.ids:
                    # Récupérer l'objet "this_p" qui est une instance de la tâche actuelle
                    this_p = self.env['project.task'].browse(tt)
                    # Si la tâche a un "kit_id", ajouter son ID à la liste "v", sinon ajouter le nom de la tâche à la liste "l"
                    if this_p.kit_id:
                        v.append(this_p.kit_id.id)
                    else:
                        l.append(this_p.name)
                        # Vérifier si la liste "v" contient des éléments
                if len(v) > 0:
                    # Effectuer une requête pour récupérer les identifiants des travaux de tâches qui correspondent aux critères
                    self.env.cr.execute(
                        'select id from project_task_work where project_id= %s and state in %s and kit_id in %s and active=True and is_copy=False',
                        (current.project_id.id, ('draft', 'affect'), tuple(v)))
                    ll = self.env.cr.fetchall()
                else:
                    # Effectuer une requête pour récupérer les identifiants des travaux de tâches qui correspondent aux critères
                    self.env.cr.execute(
                        'select id from project_task_work where project_id= %s and state in %s and etape in %s',
                        (current.project_id.id, ('draft', 'affect'), tuple(l)))

                    ll = self.env.cr.fetchall()
                    # Vérifier si la liste "l" contient des éléments
                if len(l) > 0:
                    # Effectuer une requête pour récupérer les identifiants des travaux de tâches associés à l'enregistrement actuel dans la table de relation
                    self.env.cr.execute(
                        'select project_task_work_id  from base_task_merge_automatic_wizard_project_task_work_rel where base_task_merge_automatic_wizard_id = %s ',
                        (current.id,))
                    ll1 = self.env.cr.fetchall()
                    # Vérifier si la liste "ll1" est vide
                    if not ll1:
                        raise UserError(_('Action impossible!'), _("Merci de sauvegarder le document avant!"))
                    else:
                        # Parcourir les identifiants récupérés de la table de relation et ajouter les travaux de tâches correspondants à la liste "res_cpt"
                        for nn in ll1:
                            wrk = self.env['project.task.work'].browse(nn)
                            res_cpt.append(wrk.id)
                        # Créer une intersection entre la liste "ll" et la liste "res_cpt" pour obtenir les identifiants des travaux de tâches à conserver
                    pp = set(ll).intersection(res_cpt)
                else:
                    # Si la liste "l" est vide, définir directement la liste "res_cpt" avec les identifiants récupérés
                    res_cpt = ll
                    # À ce stade, la liste "res_cpt" contient les identifiants des travaux de tâches à afficher dans le résultat
            elif current.type == '2':
                l = []
                v = []
                for tt in current.task_ids.ids:
                    ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%tt )
                    this_p = self.env['project.task'].browse(tt)
                    if this_p.kit_id:
                        v.append(this_p.kit_id.id)
                    else:
                        l.append(this_p.name)
                if len(v) > 0:
                    self.env.cr.execute(
                        'select id from project_task_work where project_id= %s and   kit_id in %s and active=True and zone=%s and secteur=%s',
                        (current.project_id.id, tuple(v), current.zone, current.secteur))
                    ll = self.env.cr.fetchall()
                else:

                    self.env.cr.execute(
                        'select id from project_task_work where project_id= %s and   active=True and zone=%s and secteur=%s and etape in %s',
                        (current.project_id.id, current.zone, current.secteur, tuple(l)))
                    ll = self.env.cr.fetchall()
                if len(l) > 0:
                    self.env.cr.execute(
                        'select project_task_work_id  from base_task_merge_automatic_wizard_project_task_work_rel where base_task_merge_automatic_wizard_id = %s ',
                        (current.id,))
                    ll1 = self.env.cr.fetchall()
                    if not ll1:
                        raise UserError(_("Action impossible!'\nMerci de sauvegarder le document avant!"))
                    else:

                        for nn in ll1:
                            wrk = self.env['project.task.work'].browse(nn)
                            res_cpt.append(wrk.id)

                    pp = set(ll).intersection(res_cpt)
                else:
                    res_cpt = ll

            ##   raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%ll)
            for kk in res_cpt:
                if kk:
                    s2 = self.env['project.task.work'].browse(kk)
                    sequence_w = 0
                    if s2.task_id:
                        self.env.cr.execute(
                            'select sequence from project_task_work where task_id=%s and sequence is not Null order by sequence desc limit 1',
                            (s2.task_id.id,))
                        res = self.env.cr.fetchone()
                    for jj in current.line_ids:
                        if jj.secteur > jj.secteur_to:
                            raise UserError(
                                _("Action impossible!\n Le secteur de départ doit etre plus petit que le secteur de fin!"))
                    for jj in current.line_ids:

                        if jj.zone == 0 and jj.secteur > 0:
                            for hh in range(jj.secteur, jj.secteur_to + 1):
                                ##sequence_w=sequence_w+1
                                if jj.employee_id:
                                    employee = jj.employee_id.id
                                else:
                                    employee = s2.employee_id.id or False
                                if jj.date_from:
                                    date_from = jj.date_from
                                else:
                                    date_from = s2.date_start
                                if jj.date_to:
                                    date_to = jj.date_to
                                else:
                                    date_to = s2.date_end
                                if jj.poteau_t:
                                    poteau_t = jj.poteau_t
                                else:
                                    poteau_t = s2.poteau_t
                                if jj.is_display is True:
                                    is_display = True
                                else:
                                    is_display = False
                                sql = """
                                            INSERT INTO base_group_merge_line2 (task_id, categ_id, product_id, name, date_start, date_end, 
                                                                               poteau_i, poteau_t, color, total_t, project_id, etape, 
                                                                               gest_id, employee_id, uom_id, uom_id_r, ftp, state, work_id, 
                                                                               sequence, zone, zo, secteur, wiz_id, is_display)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                self.env.cr.execute(sql, (s2.task_id.id, s2.categ_id.id, s2.product_id.id,
                                                          s2.name.replace(' - Secteur ' + str(s2.secteur),
                                                                          '') + ' - Secteur ' + str(
                                                              hh),
                                                          date_from, date_to, s2.poteau_t, poteau_t, s2.color,
                                                          s2.total_t,
                                                          s2.project_id.id or None, s2.etape, s2.gest_id.id or None,
                                                          employee,
                                                          s2.uom_id.id or None, s2.uom_id.id or None, s2.ftp, s2.state,
                                                          s2.id, res[0] + 1,
                                                          0, str(jj.zone), hh, current.id, is_display))



                        elif jj.zone > 0 and jj.secteur > 0:
                            for hh in range(jj.zone, jj.zone + 1):
                                for vv in range(jj.secteur, jj.secteur_to + 1):
                                    if jj.employee_id:
                                        employee = jj.employee_id.id
                                    else:
                                        employee = s2.employee_id.id or False
                                    if jj.date_from:
                                        date_from = jj.date_from
                                    else:
                                        date_from = s2.date_start
                                    if jj.date_to:
                                        date_to = jj.date_to
                                    else:
                                        date_to = s2.date_end
                                    if jj.poteau_t:
                                        poteau_t = jj.poteau_t
                                    else:
                                        poteau_t = s2.poteau_t
                                    if jj.is_display is True:
                                        is_display = True
                                    else:
                                        is_display = False
                                    sequence_w = sequence_w + 1
                                    sql = """
                                                INSERT INTO base_group_merge_line2 (task_id, categ_id, product_id, name, date_start, date_end, 
                                                                                   poteau_i, poteau_t, color, total_t, project_id, 
                                                                                   gest_id, employee_id, uom_id, uom_id_r, ftp, state, work_id, 
                                                                                   zone, secteur, wiz_id, sequence, etape, zo, is_display)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            """

                                    self.env.cr.execute(sql, (s2.task_id.id, s2.categ_id.id, s2.product_id.id,
                                                              s2.name.replace(' - Secteur ' + str(s2.secteur),
                                                                              '') + ' - Zone ' + str(
                                                                  hh) + ' - Secteur ' + str(vv),
                                                              date_from, date_to, s2.poteau_t, poteau_t, s2.color,
                                                              s2.total_t,
                                                              s2.project_id.id or None, s2.gest_id.id or None, employee,
                                                              s2.uom_id.id or None, s2.uom_id.id or None, s2.ftp,
                                                              s2.state, s2.id,
                                                              hh, vv, current.id, res[0] + 1, s2.etape, str(hh),
                                                              is_display))



                        elif jj.zone > 0 and jj.secteur == 0:
                            for hh in range(jj.zone, jj.zone + 1):
                                if jj.employee_id:
                                    employee = jj.employee_id.id
                                else:
                                    employee = s2.employee_id.id or False
                                if jj.date_from:
                                    date_from = jj.date_from
                                else:
                                    date_from = s2.date_start
                                if jj.date_to:
                                    date_to = jj.date_to
                                else:
                                    date_to = s2.date_end
                                if jj.poteau_t:
                                    poteau_t = jj.poteau_t
                                else:
                                    poteau_t = s2.poteau_t
                                if jj.is_display is True:
                                    is_display = True
                                else:
                                    is_display = False
                                sequence_w = sequence_w + 1
                                sql = """
                                            INSERT INTO base_group_merge_line2 (task_id, categ_id, product_id, name, date_start, date_end, 
                                                                               poteau_i, poteau_t, color, total_t, project_id, 
                                                                               gest_id, employee_id, uom_id, uom_id_r, ftp, state, work_id, 
                                                                               zone, zo, secteur, wiz_id, sequence, etape, is_display)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                self.env.cr.execute(sql, (s2.task_id.id, s2.categ_id.id, s2.product_id.id,
                                                          s2.name + ' - Zone ' + str(hh),
                                                          date_from, date_to, s2.poteau_t, poteau_t, s2.color,
                                                          s2.total_t,
                                                          s2.project_id.id or None, s2.gest_id.id or None, employee,
                                                          s2.uom_id.id or None, s2.uom_id.id or None, s2.ftp, s2.state,
                                                          s2.id,
                                                          hh, str(jj.hh), 0, current.id, res[0] + 1, s2.etape,
                                                          is_display))

        return True

    def apply_(self):
        current = self

        if not current.line_ids1:
            raise UserError(_("Aucune Ligne à Créer!"))

        for s2 in current.line_ids1:
            if current.exist is True:
                found = self.env['project.task.work'].search([('project_id', '=', current.project_id.id),
                                                              ('zone', '=', s2.zone),
                                                              ('secteur', '=', s2.secteur)])

            seq = s2.sequence + 1
            kk = self.env['project.task.work'].search([('project_id', '=', current.project_id.id),
                                                       ('sequence', '=', seq)])
            res_user = self.env['res.users'].browse(self.env.user.id)
            while kk:
                seq = seq + 1
                kk = self.env['project.task.work'].search([('project_id', '=', current.project_id.id),
                                                           ('sequence', '=', seq)])

            if s2.task_id.kit_id:
                self.env['project.task.work'].create({
                    'kit_id': s2.task_id.kit_id.id,
                    'task_id': s2.task_id.id,
                    'categ_id': s2.categ_id.id,
                    'product_id': s2.product_id.id,
                    'name': s2.name.replace("'", "''"),
                    'uom_id': s2.uom_id.id,
                    'date_start': s2.date_start,
                    'date_end': s2.date_end,
                    'poteau_i': s2.poteau_i,
                    'poteau_t': s2.poteau_t,
                    'color': int(s2.color),
                    'hours': s2.hours,
                    'total_t': s2.total_t,
                    'project_id': s2.project_id.id,
                    'gest_id': s2.gest_id.id,
                    'uom_id_r': s2.uom_id.id,
                    'etape': s2.etape,
                    'state': 'draft',
                    'zone': s2.zone,
                    'secteur': s2.secteur,
                    'sequence': seq,
                    'active': True,
                    'w_id': current.id,
                    'display': s2.is_display,
                    'zo': 'Zone ' + s2.zo,
                    'sect': 'Secteur ' + str(s2.secteur).zfill(2),
                    'gest_id3': int(s2.task_id.coordin_id.id),
                    'current_gest': int(s2.task_id.coordin_id.id),
                    'current_sup': int(s2.gest_id.id),
                    'reviewer_id1': int(s2.task_id.reviewer_id1.id),
                    'coordin_id1': int(s2.task_id.coordin_id1.id),
                    'coordin_id2': int(s2.task_id.coordin_id2.id),
                    'coordin_id3': int(s2.task_id.coordin_id3.id),
                    'coordin_id4': int(s2.task_id.coordin_id4.id),
                    'coordin_id5': int(s2.task_id.coordin_id5.id),
                    'coordin_id6': int(s2.task_id.coordin_id6.id),
                    'coordin_id7': int(s2.task_id.coordin_id7.id),
                    'coordin_id8': int(s2.task_id.coordin_id8.id),
                    'coordin_id9': int(s2.task_id.coordin_id9.id),
                    'coordin_id10': int(s2.task_id.coordin_id10.id),
                    'partner_id': int(s2.project_id.partner_id.id),
                    'work_orig': int(s2.id),
                })
            else:
                for s3 in current.work_ids:
                    task_work_vals = {
                        'task_id': s2.task_id.id,
                        'categ_id': s2.categ_id.id,
                        'product_id': s2.product_id.id,
                        'name': s2.name.replace("'", "''"),
                        'uom_id': s2.uom_id.id,
                        'date_start': s2.date_start,
                        'date_end': s2.date_end,
                        'poteau_i': s2.poteau_i,
                        'poteau_t': s2.poteau_t,
                        'color': int(s2.color),
                        'hours': s2.hours,
                        'total_t': s2.total_t,
                        'project_id': s2.project_id.id,
                        'gest_id': s2.gest_id.id,
                        'uom_id_r': s2.uom_id.id,
                        'etape': s2.etape,
                        'state': 'draft',
                        'zone': s2.zone,
                        'secteur': s2.secteur,
                        'sequence': seq,
                        'active': True,
                        'w_id': current.id,
                        'display': s2.is_display,
                        'zo': 'Zone ' + s2.zo,
                        'sect': 'Secteur ' + str(s2.secteur).zfill(2),
                        'gest_id3': int(s2.task_id.coordin_id.id),
                        'current_gest': int(s2.task_id.coordin_id.id),
                        'current_sup': int(s2.gest_id.id),
                        'reviewer_id1': int(s2.task_id.reviewer_id1.id),
                        'coordin_id1': int(s2.task_id.coordin_id1.id),
                        'coordin_id2': int(s2.task_id.coordin_id2.id),
                        'coordin_id3': int(s2.task_id.coordin_id3.id),
                        'coordin_id4': int(s2.task_id.coordin_id4.id),
                        'coordin_id5': int(s2.task_id.coordin_id5.id),
                        'coordin_id6': int(s2.task_id.coordin_id6.id),
                        'coordin_id7': int(s2.task_id.coordin_id7.id),
                        'coordin_id8': int(s2.task_id.coordin_id8.id),
                        'coordin_id9': int(s2.task_id.coordin_id9.id),
                        'coordin_id10': int(s2.task_id.coordin_id10.id),
                        'partner_id': int(s2.project_id.partner_id.id),
                        'work_orig': int(s2.id),
                    }
                    task_work = self.env['project.task.work'].create(task_work_vals)

                    sql_result = self.env['project.task.work'].search([('project_id', '=', s2.project_id.id),
                                                                       ('task_id', '=', s2.task_id.id),
                                                                       ('zone', '=', s2.zone),
                                                                       ('secteur', '=', s2.secteur)])
                    sql_work = self.env['work.histo'].search([('work_id', '=', s3.id)])
                    if sql_work:
                        histo_vals = {
                            'task_id': s2.task_id.id,
                            'work_id': sql_result.id,
                            'categ_id': s2.categ_id.id,
                            'product_id': s2.product_id.id,
                            'name': s2.name,
                            'work_sup_id': sql_work[0].id,
                            'date': s2.date_start,
                            'create_a': datetime.now(),
                            'create_by': res_user.employee_id.name,
                            'zone': s2.zone,
                            'secteur': s2.secteur,
                            'project_id': s2.project_id.id,
                            'partner_id': s2.project_id.partner_id.id,
                        }
                    else:
                        histo_vals = {
                            'task_id': s2.task_id.id,
                            'work_id': sql_result.id,
                            'categ_id': s2.categ_id.id,
                            'product_id': s2.product_id.id,
                            'name': s2.name,
                            'date': s2.date_start,
                            'create_a': datetime.now(),
                            'create_by': res_user.employee_id.name,
                            'zone': s2.zone,
                            'secteur': s2.secteur,
                            'project_id': s2.project_id.id,
                            'partner_id': s2.project_id.partner_id.id,
                        }
                    histo = self.env['work.histo'].create(histo_vals)

            if len(current.work_ids) > 0:
                for s3 in current.work_ids:
                    if current.type == '1':
                        s3.write({'active': False, 'w_id': current.id})
                    else:
                        if current.choix == '2':
                            s3.write({'active': False, 'w_id': current.id})
                        else:
                            s3.write({'w_id': current.id})
            else:
                v = []
                res_cpt = []
                for tt in current.task_ids.ids:
                    this_p = self.env['project.task'].browse(tt)
                    if this_p.kit_id:
                        v.append(this_p.kit_id.id)

                if v:
                    self.env.cr.execute(
                        'SELECT id FROM project_task_work WHERE project_id = %s AND state IN %s AND kit_id IN %s AND active = TRUE AND is_copy = FALSE',
                        (current.project_id.id, ('draft', 'affect'), tuple(v))
                    )
                    ll1 = self.env.cr.fetchall()

                    for nn in ll1:
                        wrk = self.env['project.task.work'].browse(nn[0])
                        res_cpt.append(wrk.id)

                    for kk in res_cpt:
                        if current.type == '1':
                            self.env['project.task.work'].browse(kk).write({'active': False, 'w_id': current.id})
                        else:
                            if current.choix == '2':
                                self.env['project.task.work'].browse(kk).write({'active': False, 'w_id': current.id})
                            else:
                                self.env['project.task.work'].browse(kk).write({'w_id': current.id})

                current.write({'state': 'open'})

                # Create records in the 'app_entity_26' and 'app_entity_26_values' tables
                view = self.env.ref(
                    'sh_message.sh_message_wizard')  # Replace 'module_name' with your actual module name
                # for jj in res_cpt:
                #     s2 = self.env['project.task.work'].browse(jj)
                #     vals = {
                #         'date_added': int(
                #             datetime.strptime(s2.date_start or s2.create_date[:10], '%Y-%m-%d').timestamp()) or '',
                #         'date_updated': int(
                #             datetime.strptime(s2.date_start or s2.create_date[:10], '%Y-%m-%d').timestamp()) or '',
                #         'created_by': 1,
                #         'parent_item_id': s2.project_id.id,
                #         'field_243': s2.name.encode('ascii', 'ignore').decode().replace("'", "\\'"),
                #         'field_253': s2.project_id.id,
                #         'field_255': s2.project_id.partner_id.id,
                #         'field_256': s2.product_id.name.encode('ascii', 'ignore').decode().replace("'", "\\'") or '',
                #         'field_260': s2.categ_id.name.encode('ascii', 'ignore').decode().replace("'", "\\'") or '',
                #         'field_261': str(s2.task_id.coordin_id.id) or '',
                #         'field_259': str(s2.gest_id.id) or '',
                #         'field_258': s2.poteau_t or 0,
                #         'field_264': int(
                #             datetime.strptime(s2.date_start_r or '2000-01-01', '%Y-%m-%d').timestamp()) or '',
                #         'field_271': int(
                #             datetime.strptime(s2.date_end_r or '2000-01-01', '%Y-%m-%d').timestamp()) or '',
                #         'field_272': str(s2.task_id.id) or '',
                #         'field_268': '72',
                #         'field_244': int(
                #             datetime.strptime(s2.date_start or s2.create_date[:10], '%Y-%m-%d').timestamp()) or '',
                #         'field_250': int(datetime.strptime(s2.date_end or '2000-01-01', '%Y-%m-%d').timestamp()) or '',
                #         'field_251': str(s2.employee_id.id) if s2.employee_id else '',
                #         'field_269': str(s2.uom_id.id) or '',
                #         'field_263': str(s2.zone) or '',
                #         'field_287': str(s2.secteur) or '',
                #         'field_273': 0,
                #         'field_274': 0,
                #     }
                #     entity_26 = self.env['app_entity_26'].create(vals)
                #
                #     field_values = [
                #         {'fields_id': 244, 'value': '72'},
                #         {'fields_id': 253, 'value': s2.project_id.id},
                #         {'fields_id': 256, 'value': s2.project_id.partner_id.id},
                #         {'fields_id': 268, 'value': s2.task_id.id}
                #     ]
                #     if s2.gest_id:
                #         field_values.append({'fields_id': 258, 'value': s2.gest_id.id})
                #     if s2.task_id.coordin_id3:
                #         field_values.append({'fields_id': 259, 'value': s2.task_id.coordin_id3.id})
                #     if s2.employee_id:
                #         field_values.append({'fields_id': 269, 'value': s2.employee_id.id})
                #
                #     for fval in field_values:
                #         self.env['app_entity_26_values'].create({
                #             'items_id': entity_26.id,
                #             'fields_id': fval['fields_id'],
                #             'value': fval['value'],
                #         })

                view_id = view and view.id or False
                return {
                    'name': 'Taches générées avec Succès',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sh.message.wizard',
                    'views': [(view_id, 'form')],
                    'view_id': view_id,
                    'target': 'new',
                    'context': self.env.context
                }

    def cancel_(self):
        current = self
        found = self.env['project.task.work'].search([('w_id', '=', current.id), ('employee_id', '!=', False)])
        if found:
            for work in found:
                raise UserError(
                    _("Attention!\nAn assignment is made with this configuration: Project %s, Zone: %s, Secteur: %s, Intervenant: %s") % (
                        current.project_id.npc, work.zone, work.secteur, work.employee_id.name))

        if self.env.cr.dbname == 'DEMO':
            found1 = self.env['project.task.work'].search([('w_id', '=', current.id), ('active', '=', True)])
            if found1:
                found1.unlink()
        # Instead of "connection.cursor()" and direct "SQL queries", use the Odoo  ORM methods available on the model.The unlink() method is used to delete records in Odoo 15.
        # In the Odoo  15 API, the "self.env" attribute is used instead of "self.pool.get()".
        # The "self.write" method has been replaced with direct assignment "(current.state = 'draft')".

        found2 = self.env['project.task.work'].search([('w_id', '=', current.id), ('active', '=', False)])
        found2.write({'active': True})

        self.env['project.task.work'].search([('w_id', '=', current.id)]).write({'w_id': False})

        current.state = 'draft'

        return {
            'name': _('Annulation faite avec Succès'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'view_id': False,
            'target': 'new',
        }

    name = fields.Char()
    disponible = fields.Boolean(compute='_compute_disponible', string='Disponible')
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    exist = fields.Boolean(string='Ids', default=True)
    year_no = fields.Char(string='Priority', default=lambda self: str(time.strftime('%Y')))
    is_kit = fields.Boolean(string="Email")
    zone = fields.Integer(string='Zone')
    secteur = fields.Integer(string='Secteur')

    project_id = fields.Many2one('project.project', string='Wizard')
    partner_id = fields.Many2one('res.partner', string='wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    product_id = fields.Many2one('product.product', string='Wizard')
    task_ids = fields.Many2many('project.task', string='Tasks')
    work_ids = fields.Many2many('project.task.work', string='Tasks')
    user_id = fields.Many2one('res.users', string='Assigned to')
    dst_task_id = fields.Many2one('project.task', string='Destination Task')
    dst_project = fields.Many2one('project.project', string='Project')
    line_ids = fields.One2many('base.task.merge.line', 'wizard_id', string='Role Lines', copy=True)
    line_ids1 = fields.One2many('base.group.merge.line2', 'wiz_id', string='Role Lines', copy=True)
    line_ids2 = fields.One2many('task_line.show.line2', 'wizard_id', string='Role Lines', copy=True)

    choix = fields.Selection([
        ('1', 'Garder Les Taches Sources Actives'),
        ('2', 'Archiver les Taches Sources')

    ],

        string='Priority', select=True)

    type = fields.Selection([
        ('1', 'Nouvelle Subdivision'),
        ('2', 'Modification Subdivision Existante'),
        ('3', 'Ajouter Subdivision A Partir d"une Existante')
    ], string='Type', select=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Validé')
    ], string='Priority', default='draft', select=True)

    week_no = fields.Selection([
        ('00', '00'),
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52')
    ], string='Priority', select=True, default=lambda self: str(time.strftime('%W')))

    keep = fields.Selection([
        ('active', 'Actives'),
        ('inactive', 'Archivées'),
        ('both', 'Actives et Archivées')
    ], string='Keep', default='active')

    def default_get(self, fields_list):
        res = super(EbMergeTasks, self).default_get(fields_list)
        # J'ai mis à jour la signature de la méthode pour utiliser fields_list.
        # De plus, j'ai remplacé res['task_ids'] = active_ids par res.update({'task_ids': active_ids})
        # pour garantir le comportement correct en cas d'autres valeurs existantes dans le dictionnaire.
        active_ids = self.env.context.get('active_ids')
        # vérifie si le modèle actif (le modèle à partir duquel cette méthode est appelée) est égal à 'project.task' et s'il existe des active_ids dans le contexte.
        if self.env.context.get('active_model') == 'project.task' and active_ids:
            # Si les conditions sont satisfaites, elle met à jour le dictionnaire res en ajoutant la clé 'task_ids' avec la valeur des active_ids.
            # La méthode update est utilisée pour garantir que les autres valeurs du dictionnaire ne sont pas écrasées.
            res.update({'task_ids': active_ids})
        return res

        # Cette méthode utilise le décorateur @api.depends pour indiquer que le calcul du champ disponible doit dépendre de la valeur du champ project_id.user_id
        # Lorsque cette méthode est exécutée, elle itère sur chaque enregistrement (book) pour effectuer les opérations suivantes :
        # vérifie si l'ID de l'utilisateur associé au champ 'user_id' de l'enregistrement 'book.project_id' est égal à l'ID de l'utilisateur actuellement connecté (self.env.user.id).
        # Si les deux ID correspondent, cela signifie que l'utilisateur actuel est associé au projet correspondant à 'book.project_id'. Dans ce cas, le champ 'disponible' de 'book' est défini sur 'True'.
        # Si les deux ID ne correspondent pas, cela signifie que l'utilisateur actuel n'est pas associé au projet correspondant à 'book.project_id'. Dans ce cas, le champ 'disponible' de book est défini sur 'False'

    @api.depends('project_id.user_id')
    def _compute_disponible(self):
        for book in self:
            if book.project_id.user_id.id == self.env.user.id:
                book.disponible = True
            else:
                book.disponible = False

    def _compute_default_flow(self):
        result = {}
        for rec in self:
            work_ids = self.env['base.flow.merge.line'].search_count([('work_id', '=', rec.id)])
            if work_ids:
                result[rec.id] = 1
            else:
                result[rec.id] = 0

        return result

    def action_merge(self):
        names = []

        if self.dst_task_id:
            names.append(self.dst_task_id.name)
        else:
            raise UserError(_('You must select a Destination Task'))

        desc = []

        desc.append(self.dst_task_id.description)
        for record in self.task_ids:
            if record.id != self.dst_task_id.id:
                names.append(record.name)
                desc.append(record.description)

        for message in self.task_ids:
            for msg_id in message.message_ids:
                msg_id.res_id = self.dst_task_id.id

        plan_hours = self.dst_task_id.planned_hours
        for hour in self.task_ids:
            for time in hour.timesheet_ids:
                plan_hours += time.planned_hours

        self.dst_task_id.planned_hours = plan_hours

        transformed_names = ', '.join(names)
        self.dst_task_id.name = transformed_names

        transformed_desc = ', '.join(desc)
        self.dst_task_id.description = transformed_desc

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for task in self.task_ids:
            task.message_post(
                body=f"This task has been merged into: {base_url}/web#id={self.dst_task_id.id}&model=project.task")

        self.task_ids.active = False
        self.dst_task_id.active = True

        if self.user_id:
            self.dst_task_id.user_id = self.user_id
        elif self.dst_task_id.user_id:
            self.dst_task_id.user_id = self.dst_task_id.user_id
        else:
            raise UserError(
                _('There is no user assigned to the merged task, and the destination task does not have an assigned user!'))

        return True

    @api.onchange('year_no', 'week_no')
    def onchange_week_(self):

        # The result variable is no longer used since the method directly assigns values to the fields.
        if self.year_no and self.week_no:  # The method now uses the self parameter to access the field values.
            d = date(self.year_no, 1, 1)
            # The date object is created using date(self.year_no, 1, 1) instead of date(int(year_no), 1, 1).
            if d.weekday() <= 3:
                d = d - timedelta(d.weekday())
                # The timedelta class is imported separately with from datetime import timedelta.
            else:
                d = d + timedelta(7 - d.weekday())
            dlt = timedelta(days=(int(self.week_no) - 1) * 7)

            self.date_from = d + dlt
            self.date_to = d + dlt + timedelta(days=6)

    @api.onchange('project_id')
    def onchange_project_id(self):

        if self.project_id:
            self.task_ids = False
            self.work_ids = False

        return {'value': {}}

    @api.onchange('exist')
    def onchange_exist(self):
        if not self.exist:
            raise UserError(
                _("Attention!\nSi vous décocher cette option, le système ne vérifiera pas l'existence du Project-Zone-Secteur!"))

    @api.onchange('project_id', 'task_ids')
    def onchange_project_id(self):

        ltask1 = []
        ltask2 = []
        zz = []

        if self.project_id:
            tt = self.env['project.task'].search([('project_id', '=', self.project_id.id)], order='sequence asc')

            for task in tt:
                if self.project_id.is_kit and task.kit_id.id not in ltask1:
                    ltask1.append(task.kit_id.id)
                    ltask2.append(task.id)
                elif 'Etape' in task.product_id.name and task.product_id.name not in ltask1:
                    ltask1.append(task.product_id.name)
                    ltask2.append(task.id)

            zz = self.env['project.task'].search([('id', 'in', ltask2)], order='sequence asc').ids

        return {'domain': {'task_ids': [('id', 'in', zz)]}}

    @api.onchange('project_id', 'task_ids', 'zone', 'secteur', 'keep', 'type')
    def onchange_categ_id(self):

        list_ = []
        list1 = []
        list2 = []
        tt = []

        task_work = self.env['project.task.work']

        if self.type == '1':
            is_kit = False

            if self.task_ids:
                for kk in self.task_ids.ids:
                    task = self.env['project.task'].browse(kk)

                    if task.kit_id:
                        is_kit = True
                        for jj in task.work_ids.ids:
                            work = task_work.browse(jj)

                            if work.kit_id.id not in list1:
                                list1.append(work.kit_id.id)
                                list2.append(work.id)
                    else:
                        list_.append(task.product_id.name)

                if is_kit:
                    tt = self.env['project.task.work'].search([('id', 'in', list2)], order='sequence asc').ids
                else:
                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('zone', '=', 0),
                        ('secteur', '=', 0),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids
            else:
                if self.project_id:
                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('is_copy', '=', False),
                        ('kit_id', '=', False),
                        ('zone', '=', 0),
                        ('secteur', '=', 0),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids

                    if not tt:
                        for task in tt:
                            work = task_work.browse(task.id)

                            if work.kit_id:
                                if work.kit_id.id not in list1:
                                    list1.append(work.id)

                        tt = self.env['project.task.work'].search([('id', 'in', list1)], order='sequence asc').ids

        else:
            if self.keep == 'active':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('active', '=', True),
                        ('secteur', '=', self.secteur)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('active', '=', True),
                            ('secteur', '=', self.secteur)
                        ], order='sequence asc').ids

            elif self.keep == 'inactive':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('active', '=', False),
                        ('secteur', '=', self.secteur)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('active', '=', False),
                            ('secteur', '=', self.secteur)
                        ], order='sequence asc').ids

            elif self.keep == 'both':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('secteur', '=', self.secteur),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('secteur', '=', self.secteur),
                            '|', ('active', '=', True), ('active', '=', False)
                        ], order='sequence asc').ids

        return {'domain': {'work_ids': [('id', 'in', tt)]}}

    def action_copy1(self):
        return super().copy()

    def action_copy(self, default=None):
        if default is None:
            default = {}

        for current in self:
            for tt in current.task_ids:
                packaging_obj = self.env['project.task']

                if current.zone == 0 and current.secteur == 0:
                    vals = {
                        'task_id': tt.id,
                        'product_id': tt.product_id.id,
                        'name': tt.name,
                        'date_start': tt.date_start,
                        'date_end': tt.date_end,
                        'poteau_t': tt.qte,
                        'color': tt.color,
                        'total_t': tt.color * 7,
                        'project_id': tt.project_id.id,
                        'gest_id': tt.reviewer_id.id or False,
                        'uom_id': tt.uom_id.id,
                        'uom_id_r': tt.uom_id.id,
                        'ftp': tt.ftp,
                        'zone': tt.zone,
                        'secteur': tt.secteur,
                        'state': 'draft',
                        'priority': tt.priority,
                    }
                    cte = packaging_obj.create(vals)

                elif current.zone > 0 and current.secteur == 0:
                    for cc in range(1, current.zone + 1):
                        vals = {
                            'task_id': tt.id,
                            'product_id': tt.product_id.id,
                            'name': tt.name + ' Zone ' + str(cc),
                            'date_start': tt.date_start,
                            'date_end': tt.date_end,
                            'poteau_t': tt.qte,
                            'color': tt.color,
                            'total_t': tt.color * 7,
                            'project_id': tt.project_id.id,
                            'gest_id': tt.reviewer_id.id or False,
                            'uom_id': tt.uom_id.id,
                            'uom_id_r': tt.uom_id.id,
                            'ftp': tt.ftp,
                            'zone': cc,
                            'secteur': 0,
                            'state': 'draft',
                            'priority': tt.priority,
                        }
                        cte = packaging_obj.create(vals)

                elif current.zone > 0 and current.secteur > 0:
                    for cc in range(1, current.zone + 1):
                        for cc1 in range(1, current.secteur + 1):
                            vals = {
                                'task_id': tt.id,
                                'product_id': tt.product_id.id,
                                'name': tt.name + ' Zone ' + str(cc) + ' Secteur ' + str(cc1),
                                'date_start': tt.date_start,
                                'date_end': tt.date_end,
                                'poteau_t': tt.qte,
                                'color': tt.color,
                                'total_t': tt.color * 7,
                                'project_id': tt.project_id.id,
                                'gest_id': tt.reviewer_id.id or False,
                                'uom_id': tt.uom_id.id,
                                'uom_id_r': tt.uom_id.id,
                                'ftp': tt.ftp,
                                'zone': cc,
                                'secteur': cc1,
                                'priority': tt.priority,
                                'state': 'draft',
                            }
                            cte = packaging_obj.create(vals)

        return cte

    def action_copy3(self):
        packaging_obj = self.env['project.task']
        packaging_copy = packaging_obj.copy(self.dst_task_id.id)
        packaging_copy.write({'name': 'dfsdf'})
        return True


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    w_id = fields.Many2one('base.task.merge.automatic.wizard', string='Company', readonly=True,
                           states={'draft': [('readonly', False)]}, )
