#Student Name
#Student ID
#Course

# Railway Management System
import os
import random
import string
import json

# File paths
STAFF_FILE = 'staff.txt'
TRAIN_FILE = 'train.txt'
BOOKING_FILE = 'booking.txt'

# Utility Functions
def generate_pnr():
    """Generate a unique 6-character alphanumeric booking reference (PNR)."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_berth_number():
    """Generate a unique 3-digit numerical berth number."""
    return str(random.randint(100, 999))

def read_file(filename):
    """Read data from a file and return a list of dictionaries."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [json.loads(line) for line in f.readlines()]
    return []

def write_file(filename, data):
    """Write a dictionary as a JSON string to a file."""
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + "\n")

# Classes and Methods
class Staff:
    """Class to handle staff data and login functionality."""
    def __init__(self, civil_id, name, role, age, address, password):
        self.civil_id = civil_id
        self.name = name
        self.role = role
        self.age = age
        self.address = address
        self.password = password

    @staticmethod
    def login(civil_id, password, role):
        """Authenticate a staff member based on Civil ID, password, and role."""
        staff_list = read_file(STAFF_FILE)
        for staff in staff_list:
            if staff['civil_id'] == civil_id and staff['password'] == password and staff['role'] == role:
                return True
        return False

class Train:
    """Class to manage train-related functionalities."""
    def __init__(self, train_number, origin, destination, total_seats, available_seats, fare):
        self.train_number = train_number
        self.origin = origin
        self.destination = destination
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.fare = fare

    @staticmethod
    def search_trains(origin, destination):
        """Search for trains based on origin and destination."""
        trains = read_file(TRAIN_FILE)
        return [train for train in trains if train['origin'] == origin and train['destination'] == destination]

    @staticmethod
    def book_train(train_number, passenger_details):
        """Book seats for passengers on a specified train."""
        trains = read_file(TRAIN_FILE)
        for train in trains:
            if train['train_number'] == train_number and train['available_seats'] >= len(passenger_details):
                train['available_seats'] -= len(passenger_details)
                write_file(BOOKING_FILE, {
                    "pnr": generate_pnr(),
                    "train_number": train_number,
                    "passenger_details": passenger_details
                })
                return True
        return False
    
    @staticmethod
    def view_train_information(train_number):
        """Display information of a specific train."""
        trains = read_file(TRAIN_FILE)
        for train in trains:
            if train['train_number'] == train_number:
                print(f"Train Number: {train['train_number']}, Origin: {train['origin']}, Destination: {train['destination']}, Total Seats: {train['total_seats']}, Available Seats: {train['available_seats']}, Fare: {train['fare']}")
                return train
        print("Train not found.")
        return None
    @staticmethod
    def cancel_train(train_number):
        """Cancel a specific train by its train number."""
        trains = read_file(TRAIN_FILE)
        updated_trains = [train for train in trains if train['train_number'] != train_number]

        if len(trains) == len(updated_trains):
            print("Train not found.")
            return False

        with open(TRAIN_FILE, 'w') as f:
            for train in updated_trains:
                f.write(json.dumps(train) + "\n")
        print(f"Train {train_number} has been canceled.")
        return True
    
    @staticmethod
    def train_report():
        """Report on trains that are booked over 90%."""
        trains = read_file(TRAIN_FILE)
        trains_over_90 = False  # Flag to track if any trains are booked over 90%

        for train in trains:
            booked_percentage = ((train['total_seats'] - train['available_seats']) / train['total_seats']) * 100
            if booked_percentage > 90:
                print(f"Train Number: {train['train_number']}, Booked Percentage: {booked_percentage:.2f}%")
                trains_over_90 = True  # Set flag to True if a train meets the criteria

        if not trains_over_90:  # If no trains were over 90% booked
            print("There are no trains booked by over 90%.")


class Passenger:
    """Class to manage passenger-related functionalities."""
    def __init__(self, civil_id, name, age, address):
        self.civil_id = civil_id
        self.name = name
        self.age = age
        self.address = address

    @staticmethod
    def civil_id_exists(civil_id):
        """Check if the Civil ID already exists."""
        bookings = read_file(BOOKING_FILE)
        for booking in bookings:
            for passenger in booking['passenger_details']:
                if passenger['civil_id'] == civil_id:
                    return True
        return False

    def book_ticket(self):
        """Book a train ticket by searching available trains for a given route."""
        origin = input("Enter Origin: ")
        destination = input("Enter Destination: ")
        available_trains = Train.search_trains(origin, destination)
        if not available_trains:
            print("No trains available for this route.")
            return False
        
        print("\nAvailable Trains:")
        for train in available_trains:
            print(f"Train Number: {train['train_number']}, Origin: {train['origin']}, Destination: {train['destination']}, Total Seats: {train['total_seats']}, Available Seats: {train['available_seats']}, Fare: {train['fare']}")

        train_number = input("Enter Train Number to Book: ")
        passenger_details = [
            {
                'civil_id': self.civil_id,
                'name': self.name,
                'age': self.age,
                'address': self.address,
                'berth_number': generate_berth_number()
            }
        ]
        return Train.book_train(train_number, passenger_details)

    @staticmethod
    def check_previous_booking(pnr):
        """Check details of a previous booking using the PNR."""
        bookings = read_file(BOOKING_FILE)
        for booking in bookings:
            if booking['pnr'] == pnr:
                print("\nBooking Details:")
                print(f"PNR: {booking['pnr']}")
                print(f"Train Number: {booking['train_number']}")
                for passenger in booking['passenger_details']:
                    print(f"Passenger Name: {passenger['name']}, Civil ID: {passenger['civil_id']}, Age: {passenger['age']}, Address: {passenger['address']}, Berth Number: {passenger['berth_number']}")
                return booking
        print("Booking not found.")
        return None

    @staticmethod
    def cancel_booking(pnr):
        """Cancel a booking using the PNR."""
        bookings = read_file(BOOKING_FILE)
        updated_bookings = []

        for booking in bookings:
            if booking['pnr'] == pnr:
                print(f"Booking with PNR {pnr} has been canceled.")
                continue  # Skip this booking
            updated_bookings.append(booking)

        with open(BOOKING_FILE, 'w') as f:
            for booking in updated_bookings:
                f.write(json.dumps(booking) + "\n")

class TicketInspector(Staff):
    """Class for Ticket Inspector with functionality to block passengers."""
    def block_passenger(self, civil_id):
        """Block a passenger by their Civil ID and update the booking file."""
        bookings = read_file(BOOKING_FILE)
        updated_bookings = []

        for booking in bookings:
            if booking['passenger_details'][0]['civil_id'] != civil_id:
                updated_bookings.append(booking)
            else:
                print(f"Passenger with Civil ID {civil_id} has been blocked.")
        
        if len(bookings) == len(updated_bookings):
            print("Passenger not found.")
        else:
            with open(BOOKING_FILE, 'w') as f:
                for booking in updated_bookings:
                    f.write(json.dumps(booking) + "\n")

# Ticket Inspector Menu
def ticket_inspector_menu(inspector):
    """Display the Ticket Inspector menu and handle user interactions."""
    while True:
        print("\nTicket Inspector Menu:\nB1. Block Passenger\nB2. Back to Previous Menu")
        choice = input("Select an option: ").upper()

        if choice == 'B1':
            civil_id = input("Enter Passenger Civil ID to Block: ")
            inspector.block_passenger(civil_id)
        elif choice == 'B2':
            break
        else:
            print("Invalid option. Please try again.")

# Passenger Menu
def passenger_menu():
    """Display the Passenger menu and handle user interactions."""
    while True:
        print("\nBooking Menu:\nA1. Search & Book Train\nA2. Check Previous Booking\nA3. Back to Main Menu")
        choice = input("Select an option: ").upper()

        if choice == 'A1':
            civil_id = input("Enter Civil ID: ")
            if Passenger.civil_id_exists(civil_id):
                print("This Civil ID is already in use. Please use a different one.")
                continue

            name = input("Enter Name: ")

            while True:
                try:
                    age = int(input("Enter Age: "))
                    break  # Exit the loop if a valid integer is entered
                except ValueError:
                    print("Invalid input. Please enter a valid number for age.")
            address = input("Enter Address: ")
            passenger = Passenger(civil_id, name, age, address)
            if not passenger.book_ticket():
                print("Booking failed. Please try again.")
        elif choice == 'A2':
            pnr = input("Enter Booking Reference (PNR): ")
            booking = Passenger.check_previous_booking(pnr)
            if booking:
                cancel_choice = input("Do you want to cancel this booking? (Y/N): ").upper()
                if cancel_choice == 'Y':
                    Passenger.cancel_booking(pnr)
        elif choice == 'A3':
            break
        else:
            print("Invalid option. Please try again.")
# Train Driver Menu
def train_driver_menu():
    """Display the Train Driver menu and handle user interactions."""
    while True:
        print("\nTrain Driver Menu:")
        print("C1. View Train Information")
        print("C2. Cancel the Train")
        print("C3. Train Report")
        print("C4. Back to Main Menu")
        choice = input("Select an option: ").upper()

        if choice == 'C1':
            train_number = input("Enter Train Number: ")
            Train.view_train_information(train_number)
        elif choice == 'C2':
            train_number = input("Enter Train Number to Cancel: ")
            Train.cancel_train(train_number)
        elif choice == 'C3':
            Train.train_report()
        elif choice == 'C4':
            break
        else:
            print("Invalid option. Please try again.")

# Main Menu
def main_menu():
    """Display the main menu and handle user interactions."""
    while True:
        print("\nMain Menu:")
        print("A. Passenger")
        print("B. Login as Ticket Inspector")
        print("C. Login as Train Driver")
        print("D. Exit")
        choice = input("Select an option: ").upper()

        if choice == 'A':
            passenger_menu()
        elif choice == 'B':
            civil_id = input("Enter Civil ID: ")
            password = input("Enter Password: ")
            role = 'Ticket Inspector'  # Fixed role for ticket inspector

            if Staff.login(civil_id, password, role):
                inspector = TicketInspector(civil_id, "", "", "", "", password)
                ticket_inspector_menu(inspector)
            else:
                print("Invalid login. Please try again.")
        elif choice == 'C':
            civil_id = input("Enter Civil ID: ")
            password = input("Enter Password: ")
            role = 'Train Driver'  # Placeholder for train driver role

            if Staff.login(civil_id, password, role):
                train_driver_menu()  # Access the train driver menu
            else:
                print("Invalid login. Please try again.")
        elif choice == 'D':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
