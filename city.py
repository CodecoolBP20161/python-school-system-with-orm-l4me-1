from models import *
from school import *


class City(BaseModel):
    name = CharField()
    school = ForeignKeyField(School, related_name='cities')
