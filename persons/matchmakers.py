from django.db.models import QuerySet
from django.utils.translation import gettext as _

from persons.enums import GenderChoices, RelationChoices, MatchingStatusChoices
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
        self.queryset = self.match_queryset()

    def match_queryset(self) -> QuerySet:
        return Person.objects.filter(
            first_name__icontains=self.person.first_name,
            last_name__icontains=self.person.last_name,
            birth_year=self.person.birth_year,
            gender=self.person.gender
        ).exclude(id=self.person.id)

    def match_exists(self) -> bool:
        return self.queryset.exists()


class RelationMatchmaker(Matchmaker):
    def __init__(self, related_person, main_person, relation):
        self.main_person = main_person
        self.relation = relation
        super().__init__(related_person)

    def match_queryset(self) -> QuerySet:
        return super().match_queryset().exclude(id=self.main_person.id)

    def related_person_match_choices(self) -> list[tuple[int, str]]:
        choices_list = [(None, _('هیچکدام'))]
        queryset = self.queryset.select_related(
            'father', 'mother'
        ).prefetch_related(
            'spouses', 'father_children', 'mother_children'
        )
        for person in queryset:
            choice_label = f'{person.first_name} {person.last_name}'
            main_person_is_father = bool(
                self.relation == RelationChoices.CHILD and self.person.gender == GenderChoices.MALE
            )
            main_person_is_mother = bool(
                self.relation == RelationChoices.CHILD and self.person.gender == GenderChoices.FEMALE
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
            # TODO Handle husband
            elif person.spouses.exclude(id=self.person.id).exists():
                spouse = person.spouses.exclude(id=self.person.id).first()
                choice_label += f' - نام یکی از همسرها: {spouse.first_name}'
            choices_list.append((person.id, choice_label))
        return choices_list

    def create_matching_request(self) -> RelationMatchingRequest:
        matching_request = RelationMatchingRequest.objects.create(
            person=self.main_person,
            related_person=self.person,
            relation=self.relation
        )
        self.person.matching_status = MatchingStatusChoices.IS_MATCHING
        self.person.save()
        return matching_request


