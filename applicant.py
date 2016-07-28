from models import *
from school import *
from city import *
from interview_slot import *
import string
import random
from person import *


class Applicant(Person):
    location = CharField()
    time = DateField()
    school = ForeignKeyField(School, related_name='applicants', null=True)
    status = IntegerField(choices=[(0, 1, 2, 3), ('new', 'in progress', 'rejected', 'accepted')])
    application_code = CharField(null=True, unique=True)

    @classmethod
    def applicants_without_applicant_code(cls):
        query = cls.select().where(cls.application_code >> None)
        if query:
            print("The following applicants have no application code: \n")
            for applicant in query:
                print(applicant.full_name)
                applicant.generate_application_code()

    def generate_application_code(self):
        generated = None
        while(generated is None or Applicant.select().where(Applicant.application_code == generated)):
            abc = [string.digits, string.ascii_uppercase, string.ascii_lowercase]
            generated = ''.join([random.choice(abc[abs(i)//2]) for i in range(-5, 6, 2)]) + "#&"
        Applicant.update(application_code=generated, status=1).where(Applicant.id == self.id).execute()

    @classmethod
    def find_closest_school(cls):
        query = cls.select().where(cls.school >> None)
        if query:
            print("The following applicants have no school connected: \n")
            for applicant in query:
                print(applicant.full_name)
                school = City.get(City.name == applicant.location).school
                cls.update(school=school).where(cls.id == applicant.id).execute()

    @classmethod
    def filter_applicant_by_school(cls, school):
        for applicant in [applicant for applicant in cls.select().where(cls.school == school)]:
            print(applicant.full_name + ": " + applicant.school.location)

    @classmethod
    def filter_applicant_by_status(cls, status):
        status_codes = {0: 'new', 1: 'in progress', 2: 'rejected', 3: 'accepted'}
        for applicant in [applicant for applicant in cls.select().where(cls.status == status)]:
            print(applicant.full_name + ": " + status_codes[applicant.status])

    @classmethod
    def filter_applicant_by_location(cls, location):
        for applicant in [applicant for applicant in cls.select().where(cls.location == location)]:
            print(applicant.full_name + ": " + applicant.location)

    @classmethod
    def filter_applicant_by_name(cls, name):
        query = cls.select().where(cls.first_name.startswith(name) | (cls.last_name.startswith(name)))
        for applicant in query:
            print(applicant.full_name)

    @classmethod
    def filter_applicant_by_email(cls, email):
        for applicant in [applicant for applicant in cls.select().where(cls.email.contains(email))]:
            print(applicant.full_name + ": " + applicant.email)
