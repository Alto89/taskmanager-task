# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)
   
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

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
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
    
    def get_absolute_url(self):
        return reverse('subdetail', kwargs={'pk': self.pk})



def post_save_user_reciever(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)
        #default_user_profile.save()
        profile.followers.add(default_user_profile.user)

post_save.connect(post_save_user_reciever, sender=User)
    


        


