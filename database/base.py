import uuid

from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, Timestamp

from core.extensions import db


Column = db.Column
relationship = relationship


class CRUDMixin(object):
    @classmethod
    def create(cls, **kwargs):
        if issubclass(cls, SurrogatePK):
            unique_id = uuid.uuid4()
            if not kwargs.get("id"):
                kwargs["id"] = unique_id
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save(commit)

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class SurrogatePK(object):
    """A mixin that adds a surrogate UUID 'primary key' column named ``id`` to
    any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(UUIDType(binary=False), primary_key=True)


class Model(CRUDMixin, db.Model, Timestamp, SurrogatePK):
    __abstract__ = True

    @classmethod
    def exists(cls, ent_id):
        result = cls.query.get(ent_id)
        return result is not None
