import sys
import os

from models import *
from applicant import *
from interview import *
from school import *


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
    choice = int(choice)

    if choice == 1:
        applicant_menu()

    if choice == 2:
        user_name = input('Enter username: ')

        if user_name == 'admin':
            pw = input('Enter password: ')
            if pw == 'admin':
                administrator_menu()
            else:
                print('Wrong password.Try again')

        else:
            print('Wrong username.Try again')

    if choice == 3:
        mentor_menu()

    elif choice == 0:
        sys.exit()

    else:
        print("Invalid number. Try again...")


def applicant_menu():
    user_name = input('Enter your e-mail: ')
    pw = input('Enter password: ')


def administrator_menu():
    a = True
    while a:
        options = ['Generate application code',
                   'Find closest school',
                   'Find interview slot',
                   'Applicants info']
        print_menu("Administrator menu", options, "Back to main menu")
        choice = int(input('Enter your choice: '))
        if choice == 1:
            Applicant.applicants_without_applicant_code()
        if choice == 2:
            Applicant.find_closest_school()
        if choice == 3:
            Interview.applicants_without_interview_slot()
        if choice == 4:
            administrator_applicants_info()
        if choice == 0:
            a = False


def administrator_applicants_info():
    admin_applicant_menu = True
    while admin_applicant_menu:
        options = ['Status', 'Time', 'Location', 'Personal data', 'School', 'Mentor name']
        print_menu("Applicants info", options, "Back to main menu")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            administrator_status()
        if choice == 2:
            print("It's time to go home :D")
        if choice == 3:
            administrator_filter_by_location()
        if choice == 4:
            administrator_filter_by_personal_data()
        if choice == 5:
            administrator_menu_applicants_school_filter()
        if choice == 6:
            administrator_mentor_applicat()
        if choice == 0:
            admin_applicant_menu = False


def administrator_status():
    status = True
    while status:
        options = ['New', 'In progress', 'Rejected', 'Accepted']
        print_menu("Filter by status", options, "Back to admin menu")
        choice = int(input("Enter your choice: \n"))
        if choice == 1:
            Applicant.filter_applicant_by_status(0)
        if choice == 2:
            Applicant.filter_applicant_by_status(1)
        if choice == 3:
            Applicant.filter_applicant_by_status(2)
        if choice == 4:
            Applicant.filter_applicant_by_status(3)
        if choice == 0:
            status = False


def administrator_menu_applicants_school_filter():
    school_filter = True
    while school_filter:
        schools = School.select()
        options = []
        for school in schools:
            options.append(school.location)
        print_menu("Filter by School", options, "Back to admin menu")
        choice = int(input('Enter your choice: \n'))
        if choice > 0 and choice <= len(options):
            Applicant.filter_applicant_by_school(schools[choice-1])
        if choice == 0:
            school_filter = False


def administrator_mentor_applicat():
    mentor_filter = True
    while mentor_filter:
        mentors = Mentor.select()
        options = []
        for mentor in mentors:
            options.append(mentor.full_name)
        print_menu("Filter by Mentor name", options, "Back to admin menu")
        choice = int(input("Enter mentor's name: \n"))
        if choice > 0 and choice <= len(options):
            Interview.filter_applicant_by_mentor(mentors[choice-1])
        if choice == 0:
            mentor_filter = False


def administrator_filter_by_location():
    location = True
    print("Press 0 to exit")
    while location:
        choice = input("Enter the city's name: \n")
        if choice == '0':
            location = False
        Applicant.filter_applicant_by_location(choice)


def administrator_filter_by_personal_data():
    personal_data = True
    while personal_data:
        options = ['Name', 'E-mail']
        print_menu("Filter by personal data", options, "Back to admin menu")
        choice = int(input("Enter your choice: \n"))
        if choice == 1:
            administrator_personal_name()
        if choice == 2:
            administrator_personal_email()
        if choice == 0:
            personal_data = False


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
    while True:
        main_menu()
        try:
            choice()
        except ValueError as err:
            print("Something went wrong. Try again")

if __name__ == '__main__':
    main()

    print_menu("Main menu", options, "Exit program")
