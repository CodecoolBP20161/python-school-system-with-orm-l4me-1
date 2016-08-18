import random
import string
import datetime
from models import *
from school import *
from city import *
from interview_slot import *
from person import *


class Applicant(Person):
    location = CharField()
    time = DateField()
    school = ForeignKeyField(School, related_name="applicants", null=True)
    status = IntegerField()
    application_code = CharField(null=True, unique=True)

    @property
    def get_status(self):
        return {0: "new", 1: "in progress", 2: "rejected", 3: "accepted"}[self.status]

    @classmethod
    def applicants_without_application_code(cls):
        query = cls.select().where(cls.application_code >> None)
        if query:
            print("Some applicants have no application code")
            if input("Want to generate it for them now? (y/n): ") == "y":
                for applicant in query:
                    applicant.generate_application_code()
                    print("{}'s application code: {}".format(applicant.full_name, applicant.application_code))

    def generate_application_code(self):
        generated = None
        while not generated or Applicant.select().where(Applicant.application_code == generated):
            abc = [string.digits, string.ascii_uppercase, string.ascii_lowercase]
            generated = "".join([random.choice(abc[abs(i)//2]) for i in range(-5, 6, 2)]) + "#&"
        self.application_code = generated
        self.status = 1
        self.save()

    @classmethod
    def applicants_without_school(cls):
        query = cls.select().where(cls.school >> None)
        if query:
            print("Some applicants have no school connected")
            if input("Want to connect them now? (y/n): ") == "y":
                for applicant in query:
                    school = City.get(City.name == applicant.location).school
                    cls.update(school=school).where(cls.id == applicant.id).execute()
                    print("{} registered in {} school.".format(applicant.full_name, school.location))

    @classmethod
    def filter_applicant_by_school(cls, school):
        query = cls.select().where(cls.school == school)
        if query:
            cls.display_applicant_list(query)
        else:
            print("No records found")

    @classmethod
    def filter_applicant_by_status(cls, status):
        query = cls.select().where(cls.status == status)
        if query:
            cls.display_applicant_list(query)
        else:
            print("No records found")

    @classmethod
    def filter_applicant_by_location(cls, location):
        print(location)
        query = cls.select().where(cls.location == location)
        if query:
            cls.display_applicant_list(query)
        else:
            print("No records found")

    @classmethod
    def filter_applicant_by_name(cls, name):
        query = cls.select().where(cls.first_name.startswith(name) | (cls.last_name.startswith(name)))
        if query:
            cls.display_applicant_list(query)
        else:
            print("No records found")

    @classmethod
    def filter_applicant_by_email(cls, email):
        query = cls.select().where(cls.email.contains(email))
        if query:
            cls.display_applicant_list(query)
        else:
            print("No records found")

    @classmethod
    def filter_applicant_by_time(cls, from_time, to_time):
        try:
            from_time = datetime.datetime.strptime(from_time, '%Y-%m-%d').date()
            to_time = datetime.datetime.strptime(to_time, '%Y-%m-%d').date()
            query = cls.select().where((cls.time >= from_time) & (cls.time <= to_time)).order_by(cls.time)
            cls.display_applicant_list(query) if query else print("No records found")
        except:
            print("Use date formatum (YYYY-MM-DD)!")

    @classmethod
    def details_of_applicant(cls, application_code):
        applicant = cls.get(cls.application_code == application_code)
        school = "not decided yet"
        if applicant.school:
            school = applicant.school.location
        print("\nStatus: {}\nAssigned school: {}\n".format(applicant.get_status, school))

    @classmethod
    def display_applicant_list(cls, applicants):
        titles = ["Full name", "E-mail", "City", "School", "Status"]
        table = [applicant.collect_data() for applicant in applicants]
        table.insert(len(table), titles)
        max_width_per_column = [max(y) for y in [[len(x[i]) for x in table] for i in range(len(table[0]))]]
        table.pop()
        print(' '.join([titles[j].ljust(k) for j, k in enumerate(max_width_per_column)]))
        print('-'*(sum(max_width_per_column)+4))
        for i in table:
            print(' '.join([i[j].ljust(k) for j, k in enumerate(max_width_per_column)]))

    def collect_data(self):
        school = "Not assigned"
        if self.school:
            school = self.school.location
        return [self.full_name, self.email, self.location, school, self.get_status]
