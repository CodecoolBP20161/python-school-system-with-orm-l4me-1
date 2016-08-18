from models import *
from interview_slot import *
from applicant import *


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name='interview')
    interview_slot = ForeignKeyField(InterviewSlot, related_name='interview')

    @classmethod
    def applicants_without_interview_slot(cls):
        for applicant in Applicant.select().where(Applicant.status == 1).order_by(Applicant.time):
            if not cls.select().where(cls.applicant == applicant.id):
                slot = InterviewSlot.find_interview_slot(applicant.school)
                if slot:
                    cls.create(applicant=applicant, interview_slot=slot)
                    booked = "New interview booked"
                else:
                    booked = "No interview slots available in this applicant's school"
                print("{}: {}".format(applicant.full_name, booked))

    @classmethod
    def filter_applicant_by_mentor(cls, mentor):
        from mentor import Mentor
        query = cls.select()
        query = [interview.applicant for interview in query if interview.interview_slot.mentor == mentor]
        if query:
            Applicant.display_applicant_list(query)

    @classmethod
    def details_of_interview(cls, application_code):
        try:
            applicant = Applicant.get(Applicant.application_code == application_code)
            cls.get(cls.applicant == applicant).interview_slot.display_details_of_interview()
        except:
            print("You have no scheduled interview yet.")
