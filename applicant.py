from models import *
from school import *


class Applicant(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    location = CharField()
    time = DateField()
    school = ForeignKeyField(School, related_name='applicants')
    status = IntegerField(choices=[(0, 1, 2, 3), ('new', 'in progress', 'rejected', 'accepted')])
    application_code = CharField(unique=True)
