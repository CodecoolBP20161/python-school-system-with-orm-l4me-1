from peewee import *

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('school_system')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db
