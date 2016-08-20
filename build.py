# This script can create the database tables based on your models

from applicant import *
from school import *
from city import *
from mentor import *
from interview_slot import *
from interview import *

def build_tables():
    db.create_tables([Applicant, School, City, Mentor, InterviewSlot, Interview], safe=True)
