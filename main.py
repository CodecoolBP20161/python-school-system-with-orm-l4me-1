import sys
import os

from models import *
from applicant import *


def print_menu(title, options, exit_message):

    counter = 1
    print (30 * '-')
    print(title)
    print (30 * '-')
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
        print ("Invalid number. Try again...")


def applicant_menu():
    user_name = input('Enter your e-mail: ')
    pw = input('Enter password: ')


def administrator_menu():
    a = True
    while a:
        options = ['Generate application code',
                   'Find closest school',
                   'Find interview slot']
        print_menu("Administrator menu", options, "Back to main menu")
        choice = int(input('Enter your choice: '))
        if choice == 1:
            Applicant.applicants_without_applicant_code()
        if choice == 2:
            Applicant.find_closest_school()
        if choice == 3:
            Applicant.applicants_without_interview_slot()
        if choice == 0:
            a = False


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
