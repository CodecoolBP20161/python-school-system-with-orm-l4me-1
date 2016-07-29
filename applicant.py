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
        query = cls.select().where(cls.school == school)
        if query:
            for applicant in query:
                print(applicant.full_name + ": " + applicant.school.location)
        else:
            print('No records found')

    @classmethod
    def filter_applicant_by_status(cls, status):
        status_codes = {0: 'new', 1: 'in progress', 2: 'rejected', 3: 'accepted'}
        query = cls.select().where(cls.status == status)
        if query:
            for applicant in query:
                print(applicant.full_name + ": " + status_codes[applicant.status])
        else:
            print('No records found')

    @classmethod
    def filter_applicant_by_location(cls, location):
        query = cls.select().where(cls.location == location)
        if query:
            for applicant in query:
                print(applicant.full_name + ": " + applicant.location)
        else:
            print('No records found')

    @classmethod
    def filter_applicant_by_name(cls, name):
        query = cls.select().where(cls.first_name.startswith(name) | (cls.last_name.startswith(name)))
        if query:
            for applicant in query:
                print(applicant.full_name)
        else:
            print('No records found')

    @classmethod
    def filter_applicant_by_email(cls, email):
        query = cls.select().where(cls.email.contains(email))
        if query:
            for applicant in [applicant for applicant in cls.select().where(cls.email.contains(email))]:
                print(applicant.full_name + ": " + applicant.email)
        else:
            print('No records found')

    @classmethod
    def filter_applicant_by_time(cls, from_time, to_time):
        query = cls.select().where((cls.time >= from_time) & (cls.time <= to_time)).order_by(cls.time)
        if query:
            for applicant in query:
                print(str(applicant.time) + ': ' + applicant.full_name)
        else:
            print('No records found')

    @classmethod
    def details_of_applicant(cls, email, pw):
        status_codes = {0: 'new', 1: 'in progress', 2: 'rejected', 3: 'accepted'}
        applicant_code = input("Enter your applicant code: ")
        for applicant in [applicant for applicant in cls.select().where(cls.email == email)]:
            if applicant.application_code == applicant_code:
                print("\nYour status is "+status_codes[applicant.status], "\nYour school is in " +
                      applicant.school.location)
            else:
                print("This code is not existing in the database, try again later :)")
