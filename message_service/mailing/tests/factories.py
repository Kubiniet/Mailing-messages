import random

from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from message_service.mailing.models import Client


class ClientFactory(DjangoModelFactory):
    """A factory for creation test model

    Args:
        DjangoModelFactory (_type_): _description_
    """

    tag = Faker("name")
    operator = random.randint(900, 1000)
    phone_number = Sequence(lambda n: "+73555%04d" % n)
    timezone = Faker("timezone")

    class Meta:
        model = Client
