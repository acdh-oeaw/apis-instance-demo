"""
Data model for this demo APIS instance
"""

from django.db import models

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation


class Profession(GenericModel, models.Model):
    """A model representing a profession or occupation."""

    name = models.CharField(max_length=1024)

    def __str__(self):  # noqa: D105
        return self.name


class Person(VersionMixin, E21_Person, AbstractEntity):
    """A model representing a person with associated professions."""

    profession = models.ManyToManyField(Profession, blank=True)


class Place(VersionMixin, E53_Place, AbstractEntity):
    """A model representing a place or location."""

    pass


class Group(VersionMixin, E74_Group, AbstractEntity):
    """A model representing a group or organization or institution."""

    pass


class IsRelatedTo(Relation):
    """A relation indicating a familial relationship between two persons."""

    subj_model = Person
    obj_model = Person

    @classmethod
    def reverse_name(self) -> str:  # noqa: D102
        return "is related to"


class IsAMemberOf(Relation):
    """A relation indicating that a person is a member of a group."""

    subj_model = Person
    obj_model = Group

    @classmethod
    def reverse_name(self) -> str:  # noqa: D102
        return "has as a member"


class WorksFor(Relation):
    """A relation indicating that a person works for a group or organization."""

    subj_model = Person
    obj_model = Group

    @classmethod
    def reverse_name(self) -> str:  # noqa: D102
        return "employs"


class LivesIn(Relation):
    """A relation indicating that a person lives in a place."""

    subj_model = Person
    obj_model = Place

    @classmethod
    def reverse_name(self) -> str:  # noqa: D102
        return "is the place of residence of"
