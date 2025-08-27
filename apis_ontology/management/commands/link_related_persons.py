from django.core.management.base import BaseCommand
from apis_ontology.models import Person, IsRelatedTo
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    """Command to link related persons based on last names."""

    def handle(self, *args, **options):  # noqa: D102
        connected_persons = []
        person_content_type = ContentType.objects.get_for_model(Person)

        for p in Person.objects.all():
            if p in connected_persons:
                continue
            related_persons = Person.objects.filter(surname=p.surname).exclude(pk=p.pk)
            for rp in related_persons:
                IsRelatedTo.objects.get_or_create(
                    subj_object_id=p.pk,
                    obj_object_id=rp.pk,
                    subj_content_type=person_content_type,
                    obj_content_type=person_content_type,
                )

            connected_persons.append(p)
