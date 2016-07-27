# This script can create the database tables based on your models

from models import *
from applicant import *
from school import *
from city import *

db.connect()
# List the tables here what you want to create...
db.create_tables([Applicant, School, City], safe=True)
