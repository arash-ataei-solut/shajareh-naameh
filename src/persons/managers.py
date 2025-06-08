from django.db import models
from django.db.models.manager import BaseManager

from persons import enums


class PersonQueryset(models.QuerySet):
    def exclude_matched_persons(self):
        return self.exclude(matching_status=enums.MatchingStatusChoices.MATCHED)
