from persons.enums import GenderChoices, RelationChoices
from persons.models import Person


def person_can_be_matched(person: Person) -> bool:
    return Person.objects.filter(
        first_name__icontains=person.first_name,
        last_name__icontains=person.last_name,
        birth_year=person.birth_year,
        gender=GenderChoices.MALE
    ).exists()


def similar_persons_choices(person: Person, relation: RelationChoices) -> list[tuple[int, str]]:
    return [(0, '')]
