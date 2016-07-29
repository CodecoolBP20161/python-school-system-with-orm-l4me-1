from models import *
from interview_slot import *
from applicant import *


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name='interview')
    interview_slot = ForeignKeyField(InterviewSlot, related_name='interview')

    @classmethod
    def applicants_without_interview_slot(cls):
        for applicant in Applicant.select().where(Applicant.status == 1).order_by(Applicant.time):
            assigned = False
            if cls.select().where(cls.applicant == applicant.id):
                assigned = True
            if not assigned:
                print(applicant.full_name+": ", end='')
                slot = InterviewSlot.find_interview_slot(applicant.school)
                if slot:
                    cls.create(applicant=applicant, interview_slot=slot)
                    print("New interview booked")
                else:
                    print("No interview slots available in this applicant's school")

    @classmethod
    def filter_applicant_by_mentor(cls, mentor):
        from mentor import Mentor
        query = cls.select()
        query = [interview.applicant for interview in query if interview.interview_slot.mentor == mentor]
        if query:
            Applicant.display_applicant_list(query)

    @classmethod
    def find_details_of_interview(cls, applicant):
        try:
            cls.get(cls.applicant == applicant).interview_slot.display_details_of_interview()
        except:
            print("You have no scheduled interview yet.")
