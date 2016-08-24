import random
import string
import datetime
from school import *
from city import *
from person import *
from email_gen import EmailGen


class Applicant(Person):
    location = CharField()
    time = DateField()
    school = ForeignKeyField(School, related_name="applicants", null=True)
    status = IntegerField()
    application_code = CharField(null=True, unique=True)

    @property
    def get_status(self):
        return {0: "new", 1: "in progress", 2: "rejected", 3: "accepted"}[self.status]

    @property
    def get_school(self):
        return self.school.location if self.school else "not assigned yet"

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
    def generate_appcode_email(cls, applicant):
        EmailGen.subject = 'CODECOOL APPLICATION STEP #1 - Your Application Code: {}'.format(applicant.application_code)
        EmailGen.reciever = applicant.email
        with open('application_code_email.html') as f:
            text = f.read().replace('{applicant_name}', applicant.full_name)
            text = text.replace('{application_code}', applicant.application_code)
            text = text.replace('{city_name}', applicant.get_school)
        EmailGen.text = text
        EmailGen.send_email()

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
                    cls.generate_appcode_email(applicant)

    @classmethod
    def filter_applicant(cls, filter_by, value, value_2=None):
        if filter_by == "school":
            query = cls.select().where(cls.school == value)
        elif filter_by == "status":
            query = cls.select().where(cls.status == value)
        elif filter_by == "location":
            query = cls.select().where(cls.location == value)
        elif filter_by == "name":
            query = cls.select().where(cls.first_name.startswith(value) | (cls.last_name.startswith(value)))
        elif filter_by == "email":
            query = cls.select().where(cls.email.contains(value))
        elif filter_by == "time":
            try:
                from_time = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                to_time = datetime.datetime.strptime(value_2, '%Y-%m-%d').date()
                query = cls.select().where((cls.time >= from_time) & (cls.time <= to_time)).order_by(cls.time)
            except:
                print("Use date formatum (YYYY-MM-DD)!")
                return
        cls.display_applicant_list(query)

    @classmethod
    def details_of_applicant(cls, application_code):
        applicant = cls.get(cls.application_code == application_code)
        print("\nStatus: {}\nAssigned school: {}".format(applicant.get_status, applicant.get_school))

    @staticmethod
    def display_applicant_list(applicants):
        if applicants:
            titles = ["Full name", "E-mail", "City", "School", "Status"]
            table = [applicant.collect_data() for applicant in applicants]
            columns = [max(y) for y in [[len(x[i]) for x in table+[titles]] for i in range(len(table[0]))]]
            print(' '.join([titles[j].ljust(k) for j, k in enumerate(columns)])+'\n'+'-'*(sum(columns)+4))
            [print(' '.join([i[j].ljust(k) for j, k in enumerate(columns)])) for i in table]
        else:
            print("No records found")

    def collect_data(self):
        return [self.full_name, self.email, self.location, self.get_school, self.get_status]

Applicant.generate_appcode_email(Applicant.select()[0])
