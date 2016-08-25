from mentor import *
from models import *
from applicant import *
from email_gen import EmailGen

class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    mentor = ForeignKeyField(Mentor)
    applicant = ForeignKeyField(Applicant, null=True)

    @classmethod
    def applicants_without_interview_slot(cls):
        for applicant in Applicant.select().where(Applicant.status == 1).order_by(Applicant.time):
            if not cls.select().where(cls.applicant == applicant.id):
                slot = cls.find_interview_slot(applicant.school)
                if slot:
                    for record in slot:
                        record.applicant = applicant
                        record.save()
                    booked = "New interview booked"
                    cls.generate_interview_email(slot)
                else:
                    booked = "No interview slots available in this applicant's school"
                print("{}: {}".format(applicant.full_name, booked))

    @classmethod
    def find_interview_slot(cls, applicant_school):
        query = cls.select().where(cls.applicant >> None).order_by(cls.start)
        if query:
            for slot in query:
                similar_slots = [i for i in query if applicant_school == i.mentor.school and i.start == slot.start]
                if len(similar_slots) > 1:
                    return similar_slots[:2]

    @classmethod
    def generate_interview_email(cls, interviews):
        applicant = interviews[0].applicant
        EmailGen.reciever = applicant.email
        EmailGen.subject = 'CODECOOL APPLICATION STEP #2 - Your Application Code: {}'.format(applicant.application_code)
        with open('applicant_interview_email.html') as f:
            text = f.read().replace('{applicant_name}', applicant.full_name)
            text = text.replace('{interview_start}', str(interviews[0].start))
            text = text.replace('{interview_end}', str(interviews[0].end))
            text = text.replace('{mentor_name}', ' and '.join(i.mentor.full_name for i in interviews))
        EmailGen.text = text
        EmailGen.send_email()
        for i in interviews:
            EmailGen.subject = 'CODECOOL - NEW INTERVIEW BOOKED - {}'.format(i.applicant.full_name)
            with open('mentor_email.html') as f:
                text = f.read().replace('{mentor_name}', i.mentor.full_name)
                text = text.replace('{applicant_name}', i.applicant.full_name)
                text = text.replace('{interview_start}', str(i.start))
                text = text.replace('{interview_end}', str(i.end))
            EmailGen.text = text
            EmailGen.send_email()

    @classmethod
    def filter_applicant_by_mentor(cls, mentor):
        Applicant.display_applicant_list(
         [interview.applicant for interview in cls.select() if interview.mentor == mentor and interview.applicant])

    @classmethod
    def details_of_interview(cls, application_code):
        try:
            applicant = Applicant.get(Applicant.application_code == application_code)
            interview = cls.get(cls.applicant == applicant)
            cls.get(cls.applicant == applicant, cls.id != interview.id).display_details_of_interview(interview)
        except:
            print("You have no scheduled interview yet.")

    @classmethod
    def filter_interview(cls, filter_by, value, value_2=None):
        if filter_by == "school":
            query = [i for i in cls.select() if i.mentor.school == value]
        elif filter_by == "mentor":
            query = cls.select().where(cls.mentor == value)
        elif filter_by == "app_code":
            query = [i for i in cls.select() if i.applicant and i.applicant.application_code == value]
        elif filter_by == "time":
            try:
                from_time = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                to_time = datetime.datetime.strptime(value_2, '%Y-%m-%d').date() + datetime.timedelta(days=1)
                query = cls.select().where((cls.start >= from_time) & (cls.start <= to_time)).order_by(cls.start)
            except:
                print("Use date formatum (YYYY-MM-DD)!")
                return
        cls.display_interview_list([i for i in query if i.applicant])

    @staticmethod
    def display_interview_list(interviews):
        if interviews:
            titles = ["Application code", "Applicant", "School", "Start", "End", "Mentor"]
            table = [interview.collect_data() for interview in interviews]
            columns = [max(y) for y in [[len(x[i]) for x in table+[titles]] for i in range(len(table[0]))]]
            print(' '.join([titles[j].ljust(k) for j, k in enumerate(columns)])+'\n'+'-'*(sum(columns)+4))
            [print(' '.join([i[j].ljust(k) for j, k in enumerate(columns)])) for i in table]
        else:
            print("No records found")

    def collect_data(self):
        applicant = self.applicant.full_name
        app_code = self.applicant.application_code
        school = self.applicant.school.location
        start = str(self.start)
        end = str(self.end)
        mentor = self.mentor.full_name
        return [app_code, applicant, school, start, end, mentor]

    def display_details_of_interview(self, interview):
        data = (str(self.start)[:-3], str(self.end)[-8:-3], self.mentor.school.location, self.mentor.full_name)
        print("\nDate: {d[0]}-{d[1]}\nLocation: {d[2]}\nMentor: {d[3]}, {0}".format(interview.mentor.full_name, d=data))
