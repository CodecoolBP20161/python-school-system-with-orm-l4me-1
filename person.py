from models import *


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
