# This script can generate example data for "City" and "InterviewSlot" models.
import csv
from applicant import *
from school import *
from city import *
from interview_slot import *
from mentor import *
from user import *
from menu import *
import random


def main():
    InterviewSlot.delete().execute()
    Applicant.delete().execute()
    City.delete().execute()
    Mentor.delete().execute()
    School.delete().execute()


def load_menustruct():
    with open("menu.csv") as f:
        data = csv.DictReader(f)
        for row in data:
            if row["input_dict"]:
                splitted = row["input_dict"].split("/")
                row["input_dict"] = {splitted[2*i]: splitted[2*i+1] for i in range(len(splitted)//2)}
            if row["filter_"]:
                row["filter_"] = row["filter_"].split("/")
            Menu.menu_struct.append(Menu(**{k: v for k, v in row.items() if v}))
    for school in School.select():
        Menu.menu_struct.append(Menu(text=school.location,
                                     parent="Applicant's School",
                                     module="Applicant",
                                     method="filter_applicant",
                                     filter_=["school", school]))
    for mentor in Mentor.select():
        Menu.menu_struct.append(Menu(text=mentor.full_name,
                                     parent="Applicant's mentor name",
                                     module="InterviewSlot",
                                     method="filter_applicant_by_mentor",
                                     filter_=[mentor]))
    for school in School.select():
        Menu.menu_struct.append(Menu(text=school.location,
                                     parent="Interview's School",
                                     module="InterviewSlot",
                                     method="filter_interview",
                                     filter_=["school", school]))
    for mentor in Mentor.select():
        Menu.menu_struct.append(Menu(text=mentor.full_name,
                                     parent="Interview's Mentor",
                                     module="InterviewSlot",
                                     method="filter_interview",
                                     filter_=["mentor", mentor]))
    return Menu.menu_struct


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

    # USER example data
    admin1 = User.create(
        user_name='admin',
        password='admin',
        access_right=0)

    # APPLICANT example data
    ap1 = Applicant.create(
        first_name='Péter',
        last_name='Kovács',
        location='Budapest',
        time='2016-04-22',
        school=budapest2016,
        status=1,
        application_code='dK85Pf#&')

    ap2 = Applicant.create(
        first_name='Judit',
        last_name='Tóth',
        location='Budapest',
        time='2016-04-24',
        status=0)

    ap3 = Applicant.create(
        first_name='Kinga',
        last_name='Ceglédi',
        location='Cegléd',
        time='2016-04-24',
        status=0)

    ap4 = Applicant.create(
        first_name='János',
        last_name='Veszprémi',
        location='Veszprém',
        time='2016-04-23',
        status=0)

    ap5 = Applicant.create(
        first_name='Ferenc',
        last_name='Váci',
        location='Vác',
        time='2016-05-02',
        status=0)

    ap6 = Applicant.create(
        first_name='Lajos',
        last_name='Győri',
        location='Győr',
        time='2016-05-04',
        status=0)

    ap7 = Applicant.create(
        first_name='Endre',
        last_name='Miskolci',
        location='Miskolc',
        time='2016-05-22',
        status=0)

    ap8 = Applicant.create(
        first_name='Lilla',
        last_name='Egri',
        location='Eger',
        time='2016-05-22',
        status=0)

    ap9 = Applicant.create(
        first_name='Zita',
        last_name='Debreceni',
        location='Debrecen',
        time='2016-05-13',
        status=0)

    ap10 = Applicant.create(
        first_name='Mateusz',
        last_name='Wojcik',
        location='Krakow',
        time='2016-06-16',
        status=0)

    ap11 = Applicant.create(
        first_name='Ania',
        last_name='Kaminski',
        location='Lublin',
        time='2016-06-20',
        status=0)

    #  MENTOR example data
    mentor1 = Mentor.create(
        first_name='Miklós',
        last_name='Beöthy',
        school=budapest2016,
        nick='Miki',
        password='mikipw')

    mentor2 = Mentor.create(
        first_name='Dániel',
        last_name='Salamon',
        school=budapest2016,
        nick='Dani',
        password='danipw')

    mentor3 = Mentor.create(
        first_name='Tamás',
        last_name='Tompa',
        school=budapest2016,
        nick='Tomi',
        password='tomipw')

    mentor4 = Mentor.create(
        first_name='Im',
        last_name='Mánuel',
        school=budapest2016,
        nick='Im',
        password='impw')

    mentor5 = Mentor.create(
        first_name='Mentor',
        last_name='Miskolci',
        school=miskolc2016,
        nick='Mentorm1',
        password='m1pw')

    mentor6 = Mentor.create(
        first_name='Mentor',
        last_name='Ezisiskolci',
        school=miskolc2016,
        nick='Mentorm2',
        password='m2pw')

    mentor6 = Mentor.create(
        first_name='Mentor',
        last_name='Krakow',
        school=krakow2016,
        nick='Mentork1',
        password='k1pw')

    mentor7 = Mentor.create(
        first_name='Mentor',
        last_name='Krakowi',
        school=krakow2016,
        nick='Mentork2',
        password='k2pw')

    mentor8 = Mentor.create(
        first_name='Mentor',
        last_name='Krakow2',
        school=krakow2016,
        nick='Mentork3',
        password='k3pw')

    mentor9 = Mentor.create(
        first_name='Mentor2',
        last_name='Ezisiskolci',
        school=miskolc2016,
        nick='Mentorm3',
        password='m3pw')

    #  INTERVIEW SLOT example data
    generated_dates = []
    for i in range(15):
        school = random.choice(School.select())
        mentors = [s for s in Mentor.select().where(Mentor.school == school)]
        start_date, start_hour = None, None
        while [start_date, start_hour] in generated_dates or not (start_date and start_hour):
            start_date = random.randint(10, 17)
            start_hour = random.randint(9, 16)
        generated_dates.append([start_date, start_hour])
        for k in range(random.randint(1, 3)):
            mentor = random.choice(mentors)
            mentors.remove(mentor)
            iv_slot = InterviewSlot.create(start='2016-06-' + str(start_date) + ' ' + str(start_hour) + ':00',
                                           end='2016-06-' + str(start_date) + ' ' + str(start_hour + 1) + ':00',
                                           mentor=mentor,
                                           available=True)

if __name__ == '__main__':
    main()
