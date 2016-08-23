from mentor import *
from models import *
from applicant import *


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
                        InterviewSlot.update(applicant=applicant).where(cls.id == record.id).execute()
                    booked = "New interview booked"
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
    def filter_applicant_by_mentor(cls, mentor):
        Applicant.display_applicant_list(
         [interview.applicant for interview in cls.select() if interview.mentor == mentor and interview.applicant])

    @classmethod
    def details_of_interview(cls, application_code):
        try:
            applicant = Applicant.get(Applicant.application_code == application_code)
            cls.get(cls.applicant == applicant).display_details_of_interview()
        except:
            print("You have no scheduled interview yet.")

    def display_details_of_interview(self):
        data = (str(self.start)[:-3], str(self.end)[-8:-3], self.mentor.school.location, self.mentor.full_name)
        print("\nDate: {d[0]}-{d[1]}\nLocation: {d[2]}\nMentor: {d[3]}".format(d=data))
