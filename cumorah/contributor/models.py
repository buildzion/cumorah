from wagtail.models import Page

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey

from cumorah.slugger import random_slug
from . import constants


class Contributor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=50)

    activation_request_notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='+')
    active = models.BooleanField(default=False)

    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, default='')
    level = models.CharField(max_length=20, choices=constants.MEMBER_CHOICES, default=constants.MEMBER_NONE)

    @property
    def can_contribute(self):
        return self.level in constants.MEMBER_PERMS_CONTRIBUTE

    @property
    def can_moderate(self):
        return self.level in constants.MEMBER_PERMS_MODERATE

    @property
    def can_admin(self):
        return self.level in constants.MEMBER_PERMS_ADMIN

    @staticmethod
    def get_random_slug():
        return random_slug('cc', 20)


class AuditEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    acting_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    relevant_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='+')

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    audit_object = GenericForeignKey('content_type', 'object_id')

    description = models.TextField()


class ProblemReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributor = models.ForeignKey('Contributor', on_delete=models.DO_NOTHING, null=True, blank=True)

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    problem_object = GenericForeignKey('content_type', 'object_id')

    complaint = models.TextField(blank=False)
