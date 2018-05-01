# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.user.username



class Task(models.Model):
    STATUS_NEW = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3
    STATUSES = (
        (STATUS_NEW, ('New')),
        (STATUS_IN_PROGRESS, ('In Progress')),
        (STATUS_COMPLETED, ('Completed')),
    )

    creator = models.ForeignKey(User, related_name='created_by')
    editor = models.ForeignKey(User, related_name='edited_by', blank=True, null=True)
    assigned = models.ForeignKey(User, related_name='assigned_to', blank=True, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #sub_task = models.ManyToManyField("Subtask", related_name='is_subtask', blank=True)
    status = models.PositiveSmallIntegerField(max_length=20, choices=STATUSES, default=STATUS_NEW)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def title(self):
        return self.name
    
    
class SubTask(models.Model):

    task = models.ForeignKey(Task)
    creator = models.ForeignKey(User, related_name='s_created_by')
    editor = models.ForeignKey(User, related_name='s_edited_by', blank=True, null=True)
    assigned = models.ForeignKey(User, related_name='s_assigned_to', blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(max_length=20, choices=Task.STATUSES, default=Task.STATUS_NEW)
    is_deleted = models.BooleanField(default=False)
    


        


