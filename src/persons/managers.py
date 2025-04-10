from django.db import models
from django.db.models.manager import BaseManager

from persons import enums


class PersonQueryset(models.QuerySet):
    def find_myself(self, first_name: str, last_name: str, father_name: str, mother_name: str) -> models.QuerySet:
        return self.filter(
            first_name__icontains=first_name, last_name__icontains=last_name,
            father__first_name__icontains=father_name, mother__first_name__icontains=mother_name
        )

    def exclude_matched_persons(self):
        return self.exclude(matching_status=enums.MatchingStatusChoices.MATCHED)


class PersonManager(BaseManager.from_queryset(PersonQueryset)):
    def find_myself(self, first_name: str, last_name: str, father_name: str, mother_name: str) -> models.QuerySet:
        return self.get_queryset().find_myself(first_name, last_name, father_name, mother_name)
