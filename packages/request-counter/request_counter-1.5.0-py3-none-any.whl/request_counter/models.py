"""models to store data to database"""
from django.conf import settings
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


class DbBaseManager(BaseManager):
    """api request manager"""

    def get_queryset(self):
        """
        Return a new QuerySet object. Subclasses can override this method to
        customize the behavior of the Manager.
        """
        database = getattr(settings, "RC_DATABASE", self._db)
        return self._queryset_class(
            model=self.model, using=database, hints=self._hints
        )


class ApiRequestManager(DbBaseManager.from_queryset(QuerySet)):
    """api request Manager"""


class ApiRequestCounter(models.Model):
    """api counter model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=200, primary_key=True)
    count = models.BigIntegerField(default=0)

    objects = ApiRequestManager()

    class Meta:
        db_table = "api_request_counter"
