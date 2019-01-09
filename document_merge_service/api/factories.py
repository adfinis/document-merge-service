from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class TemplateFactory(DjangoModelFactory):
    slug = Faker("slug")
    description = Faker("text")
    engine = Faker("word", ext_word_list=models.Template.ENGINE_CHOICES_LIST)
    template = None
    group = None

    class Meta:
        model = models.Template
