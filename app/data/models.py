from sqlalchemy import String, Integer

from database.base import Model, Column


class SampleModel(Model):
    __tablename__ = "sample_table"

    foo = Column(String)
    bar = Column(Integer)

    def __repr__(self):
        return "SampleModel: {id}".format(id=self.id)
