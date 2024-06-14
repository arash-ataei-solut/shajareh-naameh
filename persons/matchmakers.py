from django.db.models import QuerySet

from persons.enums import GenderChoices, RelationChoices
from persons.models import Person, RelationMatchingRequest


def person_can_be_matched(person: Person) -> bool:
    return Person.objects.filter(
        first_name__icontains=person.first_name,
        last_name__icontains=person.last_name,
        birth_year=person.birth_year,
        gender=GenderChoices.MALE
    ).exists()


class Matchmaker:
    def __init__(self, person: Person):
        self.person = person

    def match_queryset(self) -> QuerySet:
        return Person.objects.filter(
            first_name__icontains=self.person.first_name,
            last_name__icontains=self.person.last_name,
            birth_year=self.person.birth_year,
            gender=self.person.gender
        ).exclude(id=self.person.id)

    def match_exists(self) -> bool:
        return self.match_queryset().exists()


class RelationRequestMatchmaker(Matchmaker):
    def __init__(self, matching_request: RelationMatchingRequest):
        super().__init__(matching_request.person)
        self.matching_request = matching_request

    def related_person_match_choices(self) -> list[tuple[int, str]]:
        choices_list = []
        queryset = self.match_queryset().select_related(
            'father', 'mother'
        ).prefetch_related(
            'spouses', 'reverse_spouses', 'father_children', 'mother_children'
        )
        for person in queryset:
            choice_label = f'{person.first_name} {person.last_name}'
            main_person_is_father = bool(
                self.matching_request.relation == RelationChoices.CHILD and self.person.gender == GenderChoices.MALE
            )
            main_person_is_mother = bool(
                self.matching_request.relation == RelationChoices.CHILD and self.person.gender == GenderChoices.FEMALE
            )
            if person.father and not main_person_is_father:
                choice_label += f' - نام پدر: {person.father.first_name}'
            elif person.mother and not main_person_is_mother:
                choice_label += f' - نام مادر: {person.mother.first_name}'
            elif person.father_children.exclude(id=self.person.id).exists():
                child = person.father_children.exclude(id=self.person.id).first()
                choice_label += f' - نام یکی از فرزندان: {child.first_name}'
            elif person.mother_children.exclude(id=self.person.id).exists():
                child = person.mother_children.exclude(id=self.person.id).first()
                choice_label += f' - نام یکی از فرزندان: {child.first_name}'
            elif person.spouses.exclude(id=self.person.id).exists():
                spouse = person.spouses.exclude(id=self.person.id).first()
                choice_label += f' - نام یکی از همسرها: {spouse.first_name}'
            elif person.reverse_spouses.exclude(id=self.person.id).exists():
                spouse = person.reverse_spouses.exclude(id=self.person.id).first()
                choice_label += f' - نام یکی از همسرها: {spouse.first_name}'
            choices_list.append((person.id, choice_label))
        return choices_list

