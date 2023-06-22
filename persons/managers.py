from django.db import models


class PersonQueryset(models.QuerySet):
    def find_myself(self, first_name: str, last_name: str, father_name: str, mother_name: str) -> models.QuerySet:
        return self.filter(
            first_name__icontains=first_name, last_name__icontains=last_name,
            father__first_name__icontains=father_name, mother__first_name__icontains=mother_name
        )


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQueryset(self.model, using=self._db)

    def find_myself(self, first_name: str, last_name: str, father_name: str, mother_name: str) -> models.QuerySet:
        return self.get_queryset().find_myself(first_name, last_name, father_name, mother_name)
