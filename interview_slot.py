from mentor import *
from models import *


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    mentor = ForeignKeyField(Mentor, related_name='mentor_interviews')
    available = BooleanField()
