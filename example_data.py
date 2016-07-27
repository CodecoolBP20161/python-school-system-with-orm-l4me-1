# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from applicant import *
from school import *
from city import *

# SCHOOL example data
miskolc2016 = School.insert(location='Miskolc')
budapest2016 = School.insert(location='Budapest')
krakow2016 = School.insert(location='Krakow')
