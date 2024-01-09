from peewee import AutoField, BooleanField, IntegerField

from ..base_model import DbBaseModel


class TriggerTypeModel(DbBaseModel):
    id = AutoField(column_name="id")
    type = IntegerField(column_name="type")
    can_be_first = BooleanField(column_name="can_be_first")
