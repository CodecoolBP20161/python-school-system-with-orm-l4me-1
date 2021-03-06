from models import *
from applicant import *
from interview_slot import *
from school import *
from mentor import *
from city import *
from user import *
from example_data import *
from build import *
from email_gen import *


def login(user):
    Menu.params['user'] = input(["Username: ", "Nick: ", "Application code: "][user])
    if user == 0:
        return Menu.params['user'] == "admin" and input("Password: ") == "admin"
    elif user == 1:
        query = Mentor.select().where(Mentor.nick == Menu.params['user'])
        if query and input("Password: ") == query[0].password:
            Menu.params['user'] = query[0]
            return True
    elif user == 2:
        return Applicant.select().where(Applicant.application_code == Menu.params['user'])


def menu_logic(active):
    active.select_menu()
    choice = input("Please choose an option: ")
    options = active.submenus
    if choice == "0":
        active = active.parent or exit()
    elif not choice.isdigit() or int(choice) > len(options):
        print("Insert a valid option!")
    elif active.text != "Main menu" or login(int(choice)-1):
        selected = options[int(choice)-1]
        if selected.module:
            selected.select_menu()
        else:
            active = selected
    else:
        print("Incorrect login information!")
    menu_logic(active)


def main():
    connect_to_db()
    EmailGen.check_smtp_requirements()
    build_tables()
    if not Applicant.select() and input("Do you want to load example records? (y/n):") == "y":
        load_example_data()
        print("Example data loaded")
    load_menustruct()
    menu_logic(Menu.menu_struct[0])

if __name__ == '__main__':
    main()
