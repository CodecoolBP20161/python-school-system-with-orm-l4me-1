from person import *
from school import *


class Mentor(Person):
    school = ForeignKeyField(School, related_name='mentors')
    nick = CharField()
    password = CharField()
