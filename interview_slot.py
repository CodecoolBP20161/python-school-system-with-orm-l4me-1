from mentor import *
from models import *
import random


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    mentor = ForeignKeyField(Mentor, related_name='mentor_interviews')
    available = BooleanField()

    @classmethod
    def find_interview_slot(cls, applicant_school):
        query = cls.select().where(cls.available >> True)
        if query:
            query = [slot for slot in query if slot.mentor.school == applicant_school]
            if query:
                return random.choice(query)
