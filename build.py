# This script can create the database tables based on your models

from applicant import *
from school import *
from city import *
from mentor import *
from interview_slot import *


def build_tables():
    if not all([i.table_exists() for i in [Applicant, School, City, Mentor, InterviewSlot]]):
        db.create_tables([Applicant, School, City, Mentor, InterviewSlot], safe=True)
        print("Necessary tables created")
