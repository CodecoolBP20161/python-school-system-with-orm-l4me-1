# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from applicant import *
from school import *
from city import *
from interview_slot import *
from interview import *
from mentor import *


Interview.delete().execute()
InterviewSlot.delete().execute()
Applicant.delete().execute()
City.delete().execute()
Mentor.delete().execute()
School.delete().execute()


def load_example_data():
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
        location='Budapest',
        time='2016-04-22',
        school=budapest2016,
        status=1,
        application_code='dK85Pf#&')

    ap2 = Applicant.create(
        first_name='Judit',
        last_name='Tóth',
        email='tothjudit@cc.hu',
        location='Budapest',
        time='2016-04-24',
        status=0)

    ap3 = Applicant.create(
        first_name='Kinga',
        last_name='Ceglédi',
        email='cegledikinga@cc.hu',
        location='Cegléd',
        time='2016-04-24',
        status=0)

    ap4 = Applicant.create(
        first_name='János',
        last_name='Veszprémi',
        email='veszpremijanos@cc.hu',
        location='Veszprém',
        time='2016-04-23',
        status=0)

    ap5 = Applicant.create(
        first_name='Ferenc',
        last_name='Váci',
        email='vaciferenc@cc.hu',
        location='Vác',
        time='2016-05-02',
        status=0)

    ap6 = Applicant.create(
        first_name='Lajos',
        last_name='Győri',
        email='gyorilajos@cc.hu',
        location='Győr',
        time='2016-05-04',
        status=0)

    ap7 = Applicant.create(
        first_name='Endre',
        last_name='Miskolci',
        email='miskolciendre@cc.hu',
        location='Miskolc',
        time='2016-05-22',
        status=0)

    ap8 = Applicant.create(
        first_name='Lilla',
        last_name='Egri',
        email='egrililla@cc.hu',
        location='Eger',
        time='2016-05-22',
        status=0)

    ap9 = Applicant.create(
        first_name='Zita',
        last_name='Debreceni',
        email='debrecenizita@cc.hu',
        location='Debrecen',
        time='2016-05-13',
        status=0)

    ap10 = Applicant.create(
        first_name='Mateusz',
        last_name='Wojcik',
        email='mateuszwojcik@cc.pl',
        location='Krakow',
        time='2016-06-16',
        status=0)

    ap11 = Applicant.create(
        first_name='Ania',
        last_name='Kaminski',
        email='aniakaminski@cc.pl',
        location='Lublin',
        time='2016-06-20',
        status=0)

    #  MENTOR example data
    mentor1 = Mentor.create(
        first_name='Miklós',
        last_name='Beöthy',
        email='mikibeöthy@cc.hu',
        school=budapest2016)

    mentor2 = Mentor.create(
        first_name='Dániel',
        last_name='Salamon',
        email='danisalamon@cc.hu',
        school=budapest2016)

    mentor3 = Mentor.create(
        first_name='Tamás',
        last_name='Tompa',
        email='tomitompa@cc.hu',
        school=budapest2016)

    mentor4 = Mentor.create(
        first_name='Im',
        last_name='Mánuel',
        email='imanuel@cc.hu',
        school=budapest2016)

    mentor5 = Mentor.create(
        first_name='Mentor',
        last_name='Miskolci',
        email='miskolcimentor@cc.hu',
        school=miskolc2016)

    #  INTERVIEW SLOT example data
    iv_slot1 = InterviewSlot.create(
        start='2016-06-20 8:00',
        end='2016-06-20 9:00',
        mentor=mentor1,
        available=True)

    iv_slot2 = InterviewSlot.create(
        start='2016-06-20 10:00',
        end='2016-06-20 11:00',
        mentor=mentor2,
        available=True)

    iv_slot3 = InterviewSlot.create(
        start='2016-06-20 13:00',
        end='2016-06-20 14:00',
        mentor=mentor2,
        available=True)

    iv_slot4 = InterviewSlot.create(
        start='2016-06-20 15:00',
        end='2016-06-20 16:00',
        mentor=mentor3,
        available=True)

    iv_slot5 = InterviewSlot.create(
        start='2016-06-21 8:00',
        end='2016-06-21 9:00',
        mentor=mentor1,
        available=True)

    iv_slot6 = InterviewSlot.create(
        start='2016-06-21 10:00',
        end='2016-06-21 11:00',
        mentor=mentor3,
        available=True)

    iv_slot5 = InterviewSlot.create(
        start='2016-06-21 13:00',
        end='2016-06-21 14:00',
        mentor=mentor2,
        available=True)

    iv_slot6 = InterviewSlot.create(
        start='2016-06-21 15:00',
        end='2016-06-21 16:00',
        mentor=mentor3,
        available=True)

    iv_slot7 = InterviewSlot.create(
        start='2016-06-22 8:00',
        end='2016-06-22 9:00',
        mentor=mentor1,
        available=True)

    iv_slot8 = InterviewSlot.create(
        start='2016-06-22 10:00',
        end='2016-06-22 11:00',
        mentor=mentor4,
        available=True)

    iv_slot9 = InterviewSlot.create(
        start='2016-06-22 13:00',
        end='2016-06-22 14:00',
        mentor=mentor1,
        available=True)

    iv_slot10 = InterviewSlot.create(
        start='2016-06-22 15:00',
        end='2016-06-22 16:00',
        mentor=mentor4,
        available=True)

    iv_slot11 = InterviewSlot.create(
        start='2016-06-22 15:00',
        end='2016-06-22 16:00',
        mentor=mentor5,
        available=True)

    iv_slot12 = InterviewSlot.create(
        start='2016-06-22 15:00',
        end='2016-06-22 16:00',
        mentor=mentor5,
        available=True)
