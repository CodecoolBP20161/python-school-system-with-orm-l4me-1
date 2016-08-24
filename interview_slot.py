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
                        cls.update(applicant=applicant).where(cls.id == record.id).execute()
                        cls.generate_interview_email(record.mentor, applicant)
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

    def display_details_of_interview(self, interview):
        data = (str(self.start)[:-3], str(self.end)[-8:-3], self.mentor.school.location, self.mentor.full_name)
        print("\nDate: {d[0]}-{d[1]}\nLocation: {d[2]}\nMentor: {d[3]}, {0}".format(interview.mentor.full_name, d=data))
