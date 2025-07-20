#Name: Oneil Orr
# ID: 20245120
#Name of Course: Programming Techniques
#Name of Lecturer: Jonathan Johnson
#Semester: Summer 2025
#Due Date: July 20, 2025

#---------------------------------------------------------------------
# HOSPITAL MANAGEMENT SYSTEM / # Course: ITT103
#---------------------------------------------------------------------

#importing necessary libraries
import random
import datetime

# ======= Validators =======

# Function to generate a unique ID using a prefix (P, D, or A)
def generate_id(prefix):
    return prefix + str(random.randint(10000,99999))
    
# Checks if a specific date and time slot is available in a doctor's schedule
def is_time_available(schedule, date, time):
    return (date, time) not in schedule

# Validates that the name has at least two parts and only contains alphabetic characters
def is_valid_name(name):
    parts = name.strip().split()
    return len(parts) >= 2 and all(part.isalpha() for part in parts)

# Validates that age is a positive number
def is_valid_age(age):
    return age > 0

# Validates that a doctor's specialty contains only letters and spaces
def is_valid_specialty(specialty):
    return specialty.replace(" ", "").isalpha()

# Validates that a date is in the correct format
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

# Validates that time is in the correct 24-hour format
def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
    
# Prompts user input with validation and custom error messages
def safe_input(prompt, input_type=str, allowed_values=None, validator=None, custom_error=None):
    while True:     # Repeat until valid input is entered
        user_input = input(prompt).strip()     # Get user input and remove leading/trailing spaces
        try:
            value = input_type(user_input)      # Convert input to specified type (e.g., int, str, float)
            
             # Check if the input is among the allowed options (used for fixed responses like gender)
            if allowed_values and value.lower() not in allowed_values:
                raise ValueError(f"'{user_input}' is not a valid option.")
            
            # Using a custom validator function (e.g. is_valid_name, is_valid_date)
            if validator and not validator(value):
                raise ValueError
            return value     # If all checks pass, return the valid input
        
        except ValueError as e:
            # If input failed the allowed_values check, show a custom gender error
            if allowed_values and isinstance(e, ValueError) and "'{}'".format(user_input) in str(e):
                print(f"{user_input}? That's not a gender. Please enter 'Male' or 'Female'.")
                
            # Otherwise, display a custom error if one is provided
            elif custom_error:
                print(custom_error)
            # General fallback error message for invalid input types or validator failure
            else:
                print(f"Invalid input. Please enter a valid {input_type.__name__}.")
                
#------------------------------------------------------------------------------------------
# CLASS: Person (Parent Class) - base class for both patients and doctors
#------------------------------------------------------------------------------------------

class Person:
    def __init__(self, name, age, gender):
        self.name = name      # Stores the name of the person
        self.age = age             # Stores the age of the person
        self.gender = gender       # Stores the gender
        
    def display_info(self):
        #Displays basic information about a person (used in Patient.view_profile)
        print(f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")
        
#-------------------------------------------------------------------------------------------------
# CLASS: Patient (inherits from Person) - adds patient_id and appointment_list
#-------------------------------------------------------------------------------------------------
        
class Patient(Person):        #super class
    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)     #inheriting classes from Person
        self.patient_id = generate_id ("P")     # Assigns a unique patient ID starting with prefix 'P'
        self.appointment_list = []     # Initializes list of appointments
        
    def book_appointment(self, appointment):
        # Adds a new appointment to the patient's list
        self.appointment_list.append (appointment)
        
    def view_profile(self):
        # Displays patient profile and upcoming appointments
        print("\nPatient Profile Information")
        self.display_info()
        # Displays the unique ID for this patient
        print(f"Patient ID: {self.patient_id}")
        # Prepares to list the patient's appointments
        print("Appointments: ")
        
        # Flag to track if any active (not cancelled) appointments exist
        has_active_appointments = False

        # Loop through all appointments the patient has
        for appt in self.appointment_list:
            # Only show appointments that are still active (not cancelled)
            if appt.status != "Your Appointment is cancelled":
                print (f"Assigned to Dr. {appt.doctor.name} on {appt.date} at {appt.time}")
                has_active_appointments = True     # At least one valid appointment found
        
        # If none of the appointments were active, print that message
        if not has_active_appointments:
            print (" No active appointments. Please set an appointment.")
            
#---------------------------------------------------------------------------------------------------
# CLASS: Doctor (inherits from Person) - adds doctor_id, specialty, and schedule
#---------------------------------------------------------------------------------------------------

class Doctor (Person):
    def __init__(self, name, age, gender, specialty):  
        super().__init__(name, age, gender)
        self.doctor_id = generate_id("D")     # Assigns a unique doctor ID starting with prefix 'D'
        self.specialty = specialty     # Stores medical specialty
        self.appointments = [ ]      # Stores list of appointments       
        
    def is_available (self, date, time):
        # Checks if doctor has availability at a specific date/time
        for appt in self.appointments:
            if appt.date == date and appt.time == time and appt.status != "Your Appointment is cancelled":
                return False
        return True
    
    def view_schedule (self):
        # Prints all upcoming appointments
        print (f"=== Schedule for Dr. {self.name} ===")
        
         # Flag to check if there are any valid appointments
        has_appointments = False
      
        # Loop through the doctor's full list of appointments
        for appt in self.appointments:
            # Only display the ones that are not cancelled
            if appt.status != "Your Appointment is cancelled":
                print(f"Appointment on {appt.date} at {appt.time} with {appt.patient.name}")
                has_appointments = True     # Found at least one active appointment
        
        # If none of the appointments were active, print that message
        if not has_appointments:
            print("No active appointments.")

#--------------------------------------------------------------
# CLASS: Appointment - links patients and doctors
#--------------------------------------------------------------
        
class Appointment:
    def __init__(self, patient, doctor, date, time):
        self.appointment_id = generate_id ("A")     # Unique ID for the appointment
        self.patient = patient     # Patient object
        self.doctor = doctor       # Doctor object
        self.date = date               # Appointment date
        self.time = time               # Appointment time
        self.status = "Your Appointment is confirmed!!"       # Status of the appointment
        
    def confirm (self):
        # Prints ppointment confirmation message
        print (f"\nAppointment Confirmed! - The Appointment ID is: {self.appointment_id}")
        
    def cancel (self):
        # Changes appointment status and prints cancellation message
        self.status = "Your Appointment is cancelled"
        print (f"\nAppointment {self.appointment_id} has been cancelled")

#--------------------------------------------------------------------------------------
# CLASS: Hospital_System - manages patients, doctors, appointments
#--------------------------------------------------------------------------------------

class Hospital_System:
    def __init__ (self):
        self.patients = {}               # Dictionary to store patient objects
        self.doctors = {}                # Dictionary to store doctor objects
        self.appointments = {}    # Dictionary to store appointments by ID
        
        
    def add_patient (self, name, age, gender):
        # Registers a new patient and stores them in the dictionary
        patient = Patient (name, age, gender.capitalize())
        self.patients[patient.patient_id] = patient
        print("\n === Registration Complete === " )
        print(f"\nPatient Registered ID is: {patient.patient_id}")
        
 
    def add_doctor(self, name, age, gender, specialty):
        # Registers a new doctor and stores them in the dictionary
        doctor = Doctor (name, age, gender.capitalize(), specialty)
        self.doctors[doctor.doctor_id] = doctor
        print("\n         === Registration Complete ===         " )
        print(f"\n Doctor added successfully, Id number is : {doctor.doctor_id} ")
            
            
    def book_appointment(self, patient_id, doctor_id, date, time):
        try:
            # Check if the patient ID exists in the patient records
            if patient_id not in self.patients:
                print(" Patient ID not found.")
                return
            
            # Check if the doctor ID exists in the doctor records
            if doctor_id not in self.doctors:
                print(" Doctor ID not found.")
                return
            
            # Check if doctor is already booked for the selected time
            patient = self.patients.get(patient_id)
            doctor = self.doctors.get(doctor_id)
            
            # Create a new appointment object and store it
            if not doctor.is_available(date, time):
                print(" Doctor is already booked for this time.")
                return
            
            # Add appointment to patient and doctor records
            appointment = Appointment (patient, doctor, date, time)
            self.appointments [appointment.appointment_id] = appointment
            patient.book_appointment(appointment)
            doctor.appointments.append(appointment)
            appointment.confirm()       # Confirm appointment
              
        except Exception as e:
            # Catch unexpected errors
            print("An unexpected error occurred while booking the appointment:", str(e))  
    
    
    def cancel_appointment (self, appointment_id):
        try:
            # Retrieve the appointment object using ID
            appointment = self.appointments.get(appointment_id)
            if not appointment:     # If appointment not found, print an error
                print (" Appointment ID not found.")
                return
            
            # If appointment is already cancelled, notify the user
            if appointment.status == "Your Appointment is cancelled":
                print (" This appointment is already cancelled.")
                return
             
            # Cancel the appointment 
            appointment.cancel()
            
        except Exception as e:
            # Handle unexpected errors
            print(" An unexpected error occured while cancelling the appointment. Please try again.", str(e))
            
 
    def generate_bill (self, appointment_id):
        # Retrieve the appointment object using the ID
        appointment = self.appointments.get (appointment_id)
        
        if not appointment:     # If appointment doesn't exist
            print("Appointment ID not found.")      #print this
            return
        
        # If appointment is cancelled, do not generate a bill
        if appointment.status == "Your Appointment is cancelled":
            print("Appointment has been cancelled. Cannot generate bill.")
            return
        
        # If appointment is in a non-active state
        if appointment.status != "Your Appointment is confirmed!!":
            print("Appointment is not active.")
            return

        # Print header for the bill
        print("\n =============== Mandem Hospital Bill =============== ")
        print("                Port Antonio, Portand                                   ")
        print("                 Tel: (876) 613-8400                                   \n")
        # Patient and doctor details
        print(f"Patient: {appointment.patient.name}")
        print(f"Doctor: {appointment.doctor.name} ")
        print(f"Date & Time: {appointment.date} at {appointment.time} ")
        print("---------------------------------------------------------------------------- \n")
        
        consultation_fee = 3000.00     # Flat consultation fee
        
        # Prompt user to enter extra charges
        while True:     #loops until valid input is given
            try:
                extra_fee = float(input("Please enter additional charges (test/meds): JMD $"))
                if extra_fee < 0:
                    raise ValueError("Negative amounts are not allowed.")
                break  
            except ValueError as e:
                print("Invalid Input:", e)
        
        # Display breakdown of costs
        print(f"{'Consultation fee:':<30} JMD ${consultation_fee:,.2f}")
        print(f"{'Additional charges:':<30} JMD ${extra_fee:,.2f}")
        # Total bill (consultation fee + additional charges)
        total = consultation_fee + extra_fee
        print(f"{'Total Bill:':<30} JMD ${total:,.2f}")
        print ("\n----------------------------------------------------------------------------")
        
def main():
    hospital = Hospital_System()      # Create an instance of Hospital_System
            
    while True:
        # Display the main menu
        print ("\n===== Mandem Hospital Management System =====")
        print("\n  === Mandem Menu ===    \n ")
        
        print(" 1. Register New Patient")
        print(" 2. Add New Doctor")
        print(" 3. Book Appointment")
        print(" 4. Cancel Appointment")
        print(" 5. View Patient Profile")
        print(" 6. View Doctor Schedule")
        print(" 7. Generate Patient Bill")
        print(" 8. Exit \n")
        print("------------------------------------------------")
        
        # Prompt user to choose an option
        option = input("\n Choose an option: ").strip()
        
        # Option 1: Register a patient
        if option == "1":
            name = safe_input(
                        " Enter Patient's Full name (first and last): ",
                        str, validator=is_valid_name,
                        custom_error = "Please enter a valid name (first and last name)."
                        ).upper()
            age = safe_input(
                        " Enter your age: ",
                        int,
                        validator = is_valid_age,
                         custom_error = "Please enter a valid age (positive numbers only)."
                        )
            gender = safe_input(
                        " Enter Gender (Male/Female): ",
                        str,
                        allowed_values=["male", "female"]
                        )
            hospital.add_patient (name, age, gender)
         
        # Option 2: Register a doctor
        elif option == "2":
            name = safe_input(
                        " Enter Doctor's Full name (first and last): ",
                        str, validator=is_valid_name,
                        custom_error = "Please enter a valid name (first and last name)."
                        ).upper()
            age = safe_input(
                        " Enter Doctor's age: ",
                        int,
                        validator = is_valid_age,
                         custom_error = "Please enter a valid age (positive numbers only)."
                        )
            gender = safe_input(
                        " Enter Doctor's Gender (Male/Female): ",
                        str,
                        allowed_values=["male", "female"]
                        )
            specialty = safe_input(
                        " Enter Doctor's Specialty:" ,
                        str,  validator=is_valid_specialty,
                        custom_error = "Please enter a valid specialty (letters and spaces only)."
                        )
            hospital.add_doctor (name, age, gender, specialty)
            
        # Option 3: Book appointment
        elif option == "3":
            pid = input (" Enter Patient ID: ").strip().upper()
            did = input (" Enter Doctor ID: ").strip().upper()
            
            date = safe_input (
                " Date: (dd-mm-yyyy) : ",
                str,
                validator = is_valid_date,
                custom_error = "Please enter a valid date in DD-MM-YYYY format."
                )
            
            time = safe_input (
                " Time (HH:MM): " ,
                str,
                validator = is_valid_time,
                custom_error = "Please enter a valid time in 24-hour format (HH:MM)."
                )
            hospital.book_appointment (pid, did, date, time)
        
        # Option 4: Cancel appointment
        elif option == "4":
            appt_id = input (" Enter Appointment ID:  ").strip().upper()
            hospital.cancel_appointment (appt_id)
            
        # Option 5: View patient profile
        elif option == "5":
            pid = input (" Enter Patient ID: ").strip().upper()
            patient = hospital.patients.get(pid)
            if patient:
                patient.view_profile()
            else:
                print (" No patient found")
            
        # Option 6: View doctor's schedule
        elif option == "6":
            did = input (" Enter Doctor's ID: ").strip().upper()
            doctor = hospital.doctors.get(did)
            if doctor:
                doctor.view_schedule()
            else:
                print (" No doctor schedule found.")
                
        # Option 7: Generate a patient's bill
        elif option == "7":
            appt_id = input (" Enter Appointment ID: ").strip().upper()
            hospital.generate_bill(appt_id)
                
         # Option 8: Exit program
        elif option == "8":
            print (" Exiting system. Goodbye!")
            
            break
        
        # Invalid input handling
        else:
            print ("Invalid Option. Please enter a valid number!")
            
if __name__ == "__main__":
    main()