from models import *
from school import *
from city import *
import string
import random


class Applicant(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    # location = ForeignKeyField(City, related_name='applicants')
    time = DateField()
    # school = ForeignKeyField(School, related_name='applicants')
    status = IntegerField(choices=[(0, 1, 2, 3), ('new', 'in progress', 'rejected', 'accepted')])
    application_code = CharField(unique=True)

    @staticmethod
    def applicants_without_applicant_code():
        query = Applicant.select().where(Applicant.application_code == '')
        if query:
            print("The following applicants have no application code: \n")
            for applicant in query:
                print(applicant.first_name, applicant.last_name)
                applicant.generate_application_code()

    def generate_application_code(self):
        generated = None
        while(generated is None or Applicant.select().where(Applicant.application_code == generated)):
            abc = [string.digits, string.ascii_uppercase, string.ascii_lowercase]
            generated = ''.join([random.choice(abc[abs(i)//2]) for i in range(-5, 6, 2)]) + "#&"
        Applicant.update(application_code=generated).where(Applicant.id == self.id).execute()
