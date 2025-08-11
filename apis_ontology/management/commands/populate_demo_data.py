"""Command to populate a large amount of random data for demo purposes."""

import random
from django.core.management.base import BaseCommand
from faker import Faker

from apis_ontology.models import (
    Profession,
    Person,
    Place,
    Group,
    LivesIn,
    WorksFor,
    IsAMemberOf,
    IsRelatedTo,
)

fake = Faker("de_AT")


class Command(BaseCommand):
    """Command to populate a large amount of random data."""

    help = "Populate a large amount of demo data with random fictional entries"

    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument(
            "--persons", type=int, default=300, help="Number of persons"
        )
        parser.add_argument("--places", type=int, default=30, help="Number of places")
        parser.add_argument("--groups", type=int, default=30, help="Number of groups")
        parser.add_argument(
            "--seed", type=int, help="Optional random seed for reproducibility"
        )

    def handle(self, *args, **options):  # noqa: D102
        if options["seed"] is not None:
            random.seed(options["seed"])
            Faker.seed(options["seed"])

        self.stdout.write(self.style.NOTICE("Generating demo dataset..."))

        # --- Professions ---
        professions_list = [
            "Historian",
            "Writer",
            "Politician",
            "Scientist",
            "Artist",
            "Engineer",
            "Doctor",
            "Teacher",
            "Musician",
            "Explorer",
            "Architect",
            "Lawyer",
            "Philosopher",
            "Athlete",
        ]
        professions = {}
        for name in professions_list:
            obj, _ = Profession.objects.get_or_create(name=name)
            professions[name] = obj
        self.stdout.write(f"✔ Created {len(professions)} professions")

        # --- Places ---
        places = []
        for _ in range(options["places"]):
            place, _ = Place.objects.get_or_create(
                label=fake.city(),
                feature_code="PPLC",
            )
            places.append(place)
        self.stdout.write(f"✔ Created {len(places)} places")

        # --- Groups ---
        groups = []
        for _ in range(options["groups"]):
            group = Group.objects.get_or_create(label=fake.company())
            groups.append(group)
        self.stdout.write(f"✔ Created {len(groups)} groups")

        # --- Persons ---
        people = []
        for _ in range(options["persons"]):
            dob = fake.date_of_birth(minimum_age=20, maximum_age=80)
            gender = random.choice(["Male", "Female"])
            person, _ = Person.objects.get_or_create(
                forename=(
                    fake.first_name_male()
                    if gender == "Male"
                    else fake.first_name_female()
                ),
                surname=fake.last_name(),
                gender=gender,
            )
            person.date_of_birth = dob
            person.save()
            # Assign 1–3 random professions
            person.profession.set(
                random.sample(list(professions.values()), random.randint(1, 3))
            )
            people.append(person)
        self.stdout.write(f"✔ Created {len(people)} persons")

        # --- Relations ---
        lives_in_count = 0
        works_for_count = 0
        member_count = 0
        related_count = 0

        places = Place.objects.all()
        groups = Group.objects.all()
        for person in Person.objects.all():
            # Lives in 1 random place
            LivesIn.objects.create(subj=person, obj=random.choice(places))
            lives_in_count += 1

            # Works for a random group 50% chance
            if random.random() < 0.5:
                WorksFor.objects.create(subj=person, obj=random.choice(groups))
                works_for_count += 1

            # Is a member of a group 40% chance
            if random.random() < 0.4:
                IsAMemberOf.objects.create(subj=person, obj=random.choice(groups))
                member_count += 1

            # Related to another person 30% chance
            if random.random() < 0.3:
                other_person = random.choice(people)
                if other_person != person:
                    IsRelatedTo.objects.create(subj=person, obj=other_person)
                    related_count += 1

        self.stdout.write(f"✔ Created {lives_in_count} LivesIn relations")
        self.stdout.write(f"✔ Created {works_for_count} WorksFor relations")
        self.stdout.write(f"✔ Created {member_count} IsAMemberOf relations")
        self.stdout.write(f"✔ Created {related_count} IsRelatedTo relations")

        self.stdout.write(self.style.SUCCESS("🎉 Demo dataset created successfully"))
