from persons.enums import GenderChoices
from persons.models import Person


def father_matched(father: Person) -> bool:
    return Person.objects.filter(
        first_name__icontains=father.first_name,
        last_name__icontains=father.last_name,
        birth_year=father.birth_year,
        gender=GenderChoices.MALE
    ).exists()
