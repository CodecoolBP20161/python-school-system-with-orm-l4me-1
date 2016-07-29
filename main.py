import sys
import os

from models import *
from applicant import *
from interview import *
from interview_slot import *
from school import *
from mentor import *
from city import *


def print_menu(title, options, exit_message):

    counter = 1
    print(30 * '-')
    print(title)
    print(30 * '-')
    for i in options:
        print("("+str(counter)+")" + "\t" + str(i))
        counter += 1
    print("(0)" + "\t" + exit_message)


def main_menu():

    options = ["Applicant",
               "Administrator",
               "Mentor"]
    print_menu("Main menu", options, "Exit program")


def choice():
    choice = input('Enter your choice : ')
    if choice == '1':
        applicant_menu()
    if choice == '2':
        user_name = input('Enter username: ')
        if user_name == 'admin':
            pw = input('Enter password: ')
            if pw == 'admin':
                administrator_menu()
            else:
                print('Wrong password.Try again')
        else:
            print('Wrong username.Try again')
    if choice == '3':
        mentor_menu()
    elif choice == '0':
        sys.exit()
    else:
        print("Invalid number. Try again...")


def applicant_menu():
    email = input('\nEnter your e-mail: ')
    pw = input('Enter password: ')
    query = Applicant.select().where((Applicant.email == email) & (Applicant.password == pw))
    if query:
        Applicant.details_of_applicant(email, pw)
    else:
        print("wrong log in data")


def administrator_menu():
    a = True
    while a:
        options = ['Generate application code',
                   'Find closest school',
                   'Find interview slot',
                   'Applicants info']
        print_menu("Administrator menu", options, "Back to main menu")
        choice = input('Enter your choice: ')
        if choice == '1':
            Applicant.applicants_without_applicant_code()
        elif choice == '2':
            Applicant.find_closest_school()
        elif choice == '3':
            Interview.applicants_without_interview_slot()
        elif choice == '4':
            administrator_applicants_info()
        elif choice == '0':
            a = False
        else:
            print("Invalid number. Try again...")


def administrator_applicants_info():
    admin_applicant_menu = True
    while admin_applicant_menu:
        options = ['Status', 'Time', 'Location', 'Personal data', 'School', 'Mentor name']
        print_menu("Applicants info", options, "Back to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            administrator_status()
        if choice == '2':
            administrator_filter_by_time()
        if choice == '3':
            administrator_filter_by_location()
        if choice == '4':
            administrator_filter_by_personal_data()
        if choice == '5':
            administrator_menu_applicants_school_filter()
        if choice == '6':
            administrator_mentor_applicant()
        if choice == '0':
            admin_applicant_menu = False
        else:
            print("Invalid number. Try again...")


def administrator_status():
    status = True
    while status:
        options = ['New', 'In progress', 'Rejected', 'Accepted']
        print_menu("Filter by status", options, "Back to admin menu")
        choice = input("Enter your choice: \n")
        if choice == '1':
            Applicant.filter_applicant_by_status(0)
        if choice == '2':
            Applicant.filter_applicant_by_status(1)
        if choice == '3':
            Applicant.filter_applicant_by_status(2)
        if choice == '4':
            Applicant.filter_applicant_by_status(3)
        if choice == '0':
            status = False
        else:
            print("Invalid number. Try again...")


def administrator_menu_applicants_school_filter():
    school_filter = True
    while school_filter:
        schools = School.select()
        options = []
        for school in schools:
            options.append(school.location)
        print_menu("Filter by School", options, "Back to admin menu")
        choice = input('Enter your choice: \n')
        if choice in [str(i) for i in range(len(schools)+1)]:
            Applicant.filter_applicant_by_school(schools[choice-1])
        elif choice == "0":
            school_filter = False
        else:
            print("Invalid number. Try again...")


def administrator_mentor_applicant():
    mentor_filter = True
    while mentor_filter:
        mentors = Mentor.select()
        options = []
        for mentor in mentors:
            options.append(mentor.full_name)
        print_menu("Filter by Mentor name", options, "Back to admin menu")
        choice = input("Enter mentor's name: \n")
        if choice in [str(i) for i in range(len(mentors)+1)]:
            Interview.filter_applicant_by_mentor(mentors[choice-1])
        if choice == "0":
            mentor_filter = False
        else:
            print("Invalid number. Try again...")


def administrator_filter_by_location():
    location = True
    while location:
        choice = input("Enter the city's name: \n")
        if choice == '0':
            location = False
        Applicant.filter_applicant_by_location(choice)


def administrator_filter_by_time():
    time = True
    while time:
        start = input("Enter start date (YYYY-MM-DD):")
        end = input("Enter end date (YYYY-MM-DD):")
        if start == '0' or end == '0':
            time = False
        else:
            Applicant.filter_applicant_by_time(start, end)


def administrator_filter_by_personal_data():
    personal_data = True
    while personal_data:
        options = ["Name", "E-mail"]
        print_menu("Filter by personal data", options, "Back to admin menu")
        choice = input("Enter your choice: \n")
        if choice == "1":
            administrator_personal_name()
        if choice == "2":
            administrator_personal_email()
        if choice == "0":
            personal_data = False
        else:
            print("Invalid number. Try again...")


def administrator_personal_name():
    name = input("Enter the name: \n")
    Applicant.filter_applicant_by_name(name)


def administrator_personal_email():
    email = input("Enter the email: \n")
    Applicant.filter_applicant_by_email(email)


def mentor_menu():
    user_name = input('Enter your e-mail: ')
    pw = input('Enter password: ')


def main():
    if connect_to_db():
        existing_tables = True
        models = [Applicant, School, City, Mentor, InterviewSlot, Interview]
        for table in models:
            existing_tables = existing_tables and table.table_exists()
            if existing_tables:
                filled_tables = True
                for table in models[:-1]:
                    filled_tables = filled_tables and table.select()
                    if not filled_tables:
                        loading = input("Do you want to load example records? (y/n):")
                        if loading == "y":
                            from example_data import load_example_data
                            load_example_data()
                    while True:
                        main_menu()
                        try:
                            choice()
                        except ValueError as err:
                            print("Something went wrong. Try again")
            else:
                from build import build_tables
                build_tables()
                print("Necessary tables created")
                main()
    else:
        print("'school_system' database needed. Please create database first")

if __name__ == '__main__':
    main()
