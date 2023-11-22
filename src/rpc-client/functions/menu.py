import os
import time
from functions.send_file import send_file
from functions.server_files import server_files
from functions.delete_file_server import delete_file_server

def menu():
    while True:
        print("\nRPC Client Menu:")
        print("1 - Send file")
        print("2 - View files on server")
        print("3 - Query files")
        print("0 - Exit")

        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "1":
            send_file_menu()
        elif choice == "2":
            view_files_menu()
        elif choice == "3":
            query_files_menu()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def send_file_menu():
    while True:
        print("\nSend file:")

        files = os.listdir("/data")
        file_counter = 0
        for file in files:
            file_counter += 1
            print(f"{file_counter}. {file}")
        print("0 - Exit")

        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "0":
            break
        elif choice.isdigit() and int(choice) <= file_counter:
            file_name = files[int(choice) - 1]
            print(send_file(file_name))
            time.sleep(3)
            break
        else:
            print("Invalid choice. Please try again.")

def view_files_menu():
    file_counter = 0
    while True:
        print("\nView files on server:")
        for file in server_files():
            file_counter += 1
            print(f"{file_counter}. {file[1]}")
        print("0 - Exit")

        choice = input("Delete file or press 0 to go back: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "0":
            break
        elif choice.isdigit() and int(choice) <= file_counter:
            file_id = server_files()[int(choice) - 1][0]
            print(delete_file_server(file_id))
            time.sleep(3)
            break
        else:
            print("Invalid choice. Please try again.")

def query_files_menu():
    pass