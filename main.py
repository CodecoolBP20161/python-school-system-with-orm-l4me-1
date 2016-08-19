import sys
from models import *
from applicant import *
from interview import *
from interview_slot import *
from school import *
from mentor import *
from city import *
from example_data import *
from build import *


def login(user):
    Menu.params['user'] = input(["Username: ", "Nick: ", "Application code: "][user])
    if user == 0:
        passw = input("Password: ")
        if Menu.params['user'] == "admin" and passw == "admin":
            return True
    if user == 2:
        return Applicant.select().where(Applicant.application_code == Menu.params['user'])

def menu_logic():
    active = Menu.menu_struct[0]
    while True:
        active.select_menu()
        choice = input("Please choose an option: ")
        options = active.submenus
        if choice == "0":
            active.delete_params()
            active = active.parent or sys.exit()
        elif not choice.isdigit() or int(choice) > len(options):
            print("Insert a valid option!")
        elif active.text != "Main menu" or login(int(choice)-1):
            selected = options[int(choice)-1]
            if not selected.module:
                active = selected
            else:
                selected.select_menu()
        else:
            print("Incorrect login information!")


def main():
    if connect_to_db():
        if all([i.table_exists() for i in [Applicant, School, City, Mentor, InterviewSlot, Interview]]):
            if not Applicant.select() and input("Do you want to load example records? (y/n):") == "y":
                load_example_data()
            load_menustruct()
            menu_logic()
        else:
            build_tables()
            print("Necessary tables created")
            main()
    else:
        print("'school_system' database needed. Please create database first")

if __name__ == '__main__':
    main()
