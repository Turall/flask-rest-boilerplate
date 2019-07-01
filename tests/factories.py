import random

import factory
from faker import Factory as FakerFactory
from faker.providers import BaseProvider

from core.extensions import db
from app.data.models import SampleModel

faker = FakerFactory.create()


class StatusProvider(BaseProvider):
    def status(self):
        return random.choice(["active", "inactive"])


faker.add_provider(StatusProvider)


class SQLAlchemyModelFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = db.session
        session.begin(nested=True)
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj


class SampleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SampleModel

    id = factory.LazyAttribute(lambda x: faker.uuid4())
    foo = factory.LazyAttribute(lambda x: faker.name())
    bar = factory.LazyAttribute(lambda x: faker.pyint())
