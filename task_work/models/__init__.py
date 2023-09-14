# -*- coding: utf-8 -*-

from . import taskWork
from . import intervenants_affecte


# class TaskWork(models.Model):
#     _inherit = 'project.task.work'
#
#     def create(self, values):
#         if self.env.context.get('explicit_create', False):
#             # This means create is explicitly called, proceed with creation
#             return super(TaskWork, self).create(values)
#         else:
#             # Create is not explicitly called, do nothing
#             return self.env['project.task.work']
#
# # Usage:
# project_task_work = self.env['project.task.work']
# new_work = project_task_work.with_context(explicit_create=True).create({
#     'name': work.name
# })
