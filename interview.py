from models import *
from interview_slot import *
from applicant import *


class Interview(BaseModel):
    application_code = ForeignKeyField(Applicant, to_field='application_code', related_name='interview')
    interview_detail = ForeignKeyField(InterviewSlot, related_name='interview')

    @classmethod
    def assign_interview_to_new_applicant(cls, app, slot):
        cls.create(application_code=app, interview_detail=slot)
