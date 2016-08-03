from django.conf import settings
from django.db import models
from django.utils import timezone


class AllocationSource(models.Model):
    name = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)
    compute_allowed = models.IntegerField()
    # The remaining fields will be 'derived' or 'materialized' from a separate view of the 'events' class
    # compute_used
    # compute_remaining
    # user_burn_rate
    # global_burn_rate
    # time_to_zero
    #
    class Meta:
        db_table = 'allocation_source'
        app_label = 'core'

class UserAllocationSource(models.Model):
    """
    This table keeps track of whih allocation sources belong to an AtmosphereUser.

    NOTE: This table is basically a cache so that we do not have to query out to the
    "Allocation Source X" API endpoint each call.
          It is presumed that this table will be *MAINTAINED* regularly via periodic task.
    """

    user = models.ForeignKey("AtmosphereUser")
    allocation_source = models.ForeignKey(AllocationSource)

    class Meta:
        db_table = 'user_allocation_source'
        app_label = 'core'
