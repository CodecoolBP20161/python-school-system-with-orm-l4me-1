from models import *
from interview_slot import *
from applicant import *


class Interview(BaseModel):
    application_code = ForeignKeyField(Applicant, to_field='application_code', related_name='interview')
    interview_detail = ForeignKeyField(InterviewSlot, related_name='interview')

    @classmethod
    def applicants_without_interview_slot(cls):
        for applicant in Applicant.select().where(Applicant.status == 1):
            assigned = False
            if cls.select().where(cls.application_code == applicant.application_code):
                assigned = True
            if not assigned:
                print(applicant.full_name+": ", end='')
                slot = InterviewSlot.find_interview_slot(applicant.school)
                if slot:
                    cls.create(application_code=applicant, interview_detail=slot)
                    print("New interview booked")
                else:
                    print("No interview slots available in this applicant's school")
