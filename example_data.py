# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from applicant import *
from school import *
from city import *

# Applicant.delete().execute()
# City.delete().execute()
# School.delete().execute()

# SCHOOL example data
miskolc2016 = School.create(location='Miskolc')
budapest2016 = School.create(location='Budapest')
krakow2016 = School.create(location='Krakow')

# CITY example data
budapest = City.create(name='Budapest', school=budapest2016)
cegled = City.create(name='Cegléd', school=budapest2016)
veszprem = City.create(name='Veszprém', school=budapest2016)
vac = City.create(name='Vác', school=budapest2016)
gyor = City.create(name='Győr', school=budapest2016)
miskolc = City.create(name='Miskolc', school=miskolc2016)
eger = City.create(name='Eger', school=miskolc2016)
debrecen = City.create(name='Debrecen', school=miskolc2016)
krakow = City.create(name='Krakow', school=krakow2016)
lublin = City.create(name='Lublin', school=krakow2016)

# APPLICANT example data
ap1 = Applicant.create(
    first_name='Péter',
    last_name='Kovács',
    email='kovacspeter@cc.hu',
    password='kovacspeter1',
    location=budapest,
    time='2016-04-22',
    school=budapest2016,
    status=0,
    application_code='dK85Pf#&')

ap2 = Applicant.create(
    first_name='Judit',
    last_name='Tóth',
    email='tothjudit@cc.hu',
    password='tothjudit2',
    location=budapest,
    time='2016-04-24',
    status=0)

ap3 = Applicant.create(
    first_name='Kinga',
    last_name='Ceglédi',
    email='cegledikinga@cc.hu',
    password='cegledikinga3',
    location=cegled,
    time='2016-04-24',
    status=0)

ap4 = Applicant.create(
    first_name='János',
    last_name='Veszprémi',
    email='veszpremijanos@cc.hu',
    password='veszpremijanos4',
    location=veszprem,
    time='2016-04-23',
    status=0)

ap5 = Applicant.create(
    first_name='Ferenc',
    last_name='Váci',
    email='vaciferenc@cc.hu',
    password='vaciferenc5',
    location=vac,
    time='2016-05-02',
    status=0)

ap6 = Applicant.create(
    first_name='Lajos',
    last_name='Győri',
    email='gyorilajos@cc.hu',
    password='gyorilajos6',
    location=gyor,
    time='2016-05-04',
    status=0)

ap7 = Applicant.create(
    first_name='Endre',
    last_name='Miskolci',
    email='miskolciendre@cc.hu',
    password='miskolciendre7',
    location=miskolc,
    time='2016-05-22',
    status=0)

ap8 = Applicant.create(
    first_name='Lilla',
    last_name='Egri',
    email='egrililla@cc.hu',
    password='egrililla8',
    location=eger,
    time='2016-05-22',
    status=0)

ap9 = Applicant.create(
    first_name='Zita',
    last_name='Debreceni',
    email='debrecenizita@cc.hu',
    password='debrecenizita9',
    location=debrecen,
    time='2016-05-13',
    status=0)

ap10 = Applicant.create(
    first_name='Mateusz',
    last_name='Wojcik',
    email='mateuszwojcik@cc.pl',
    password='mateuszwojcik10',
    location=krakow,
    time='2016-06-16',
    status=0)

ap11 = Applicant.create(
    first_name='Ania',
    last_name='Kaminski',
    email='aniakaminski@cc.pl',
    password='aniakaminski11',
    location=lublin,
    time='2016-06-20',
    status=0)
