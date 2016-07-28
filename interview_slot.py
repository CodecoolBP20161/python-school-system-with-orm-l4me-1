from mentor import *
from models import *


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    mentor = ForeignKeyField(Mentor, related_name='mentor_interviews')
    available = BooleanField()

    @classmethod
    def find_interview_slot(cls, applicant_school):
        query = cls.select().where(cls.available >> True).order_by(InterviewSlot.start)
        if query:
            query = [slot for slot in query if slot.mentor.school == applicant_school]
            if query:
                InterviewSlot.update(available=False).where(InterviewSlot.id == query[0].id).execute()
                return query[0]
