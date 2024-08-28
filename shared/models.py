"""
Shared Models Module.

This module contains abstract Django
models that encapsulate common fields
and behaviors shared among multiple models in the project.
"""

from django.db import models


class TimeStampModel(models.Model):
    """
    Abstract model with timestamp fields (created_at and updated_at).

    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Class meta for TimeStampModel model."""

        ordering = ("-created_at",)
        abstract = True
