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
    location = ForeignKeyField(City, related_name='applicants')
    time = DateField()
    school = ForeignKeyField(School, related_name='applicants', null=True)
    status = IntegerField(choices=[(0, 1, 2, 3), ('new', 'in progress', 'rejected', 'accepted')])
    application_code = CharField(null=True)

    @staticmethod
    def applicants_without_applicant_code():
        query = Applicant.select().where(Applicant.application_code >> None)
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
        Applicant.update(application_code=generated, status=1).where(Applicant.id == self.id).execute()

    @staticmethod
    def find_closest_school():
        query = Applicant.select().where(Applicant.school >> None)
        if query:
            print("The following applicants have no school connected: \n")
            for applicant in query:
                print(applicant.first_name, applicant.last_name)
                Applicant.update(school=applicant.location.school).where(Applicant.id == applicant.id).execute()
