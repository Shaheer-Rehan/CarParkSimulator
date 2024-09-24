import random, string, bisect, time, csv, os

parking_lot = {} #dictionary to store vehicle objects
count = 0 #counter for vehicle objects
max_spaces = 8 #maximum number of parking spaces

class vehicle(): #class for vehicle objects
    spaces = list(range(1,9)) #list of parking spaces
    
    def __init__(self, reg_no, count, choice): #constructor for vehicle objects
        self.reg_no = reg_no
        self.count = count
        self.choice = choice
        self.timestamp = time.time()
        self.ticket = None
        self.ID = None
        self.enter = None
        self.exit = None
    
    def __str__(self): #string method for printing vehicle objects
        return (
            f"\nVehicle Registration No.: {self.reg_no} \nParking Ticket No.: {self.ticket_no()}"
            f"\nParking Space ID: {self.return_ID()} \nRemaining Parking Spaces: {len(self.available_space())}"
            f"\nEntry Time: {self.entry_time_print()} \nExit Time: {self.exit_time_print()} \nParking fee: {self.fee()}"
        )

    #This method is crucial for determining the no. of available spaces in the parking lot. Using the timestamp, the vehicle object with the latest timestamp can be identified, 
    #and the updated value of available spaces can be returned
    def update_timestamp(self, val):                              
        self.timestamp = val
        return self.timestamp
    
    def ticket_no(self): #method to generate random ticket number
        if self.ticket is None:
            char = string.digits
            rand = "".join(random.choice(char) for i in range(4))
            self.ticket = f"{rand} {self.reg_no}" #???
            return self.ticket
        else:
            return self.ticket
    
    def parking_space_ID(self): #method to generate random parking space ID and to update the list of available parking spaces
        if self.ID is None:
            self.ID = random.choice(vehicle.spaces)
        if self.exit_status() is False and self.ID in vehicle.spaces: #what to do when choice ==4 for car still in parking lot
            vehicle.spaces.remove(self.ID)
        return self.ID, vehicle.spaces #returns a tuple
    
    def return_ID(self):
        self.ID = self.parking_space_ID()[0]
        return self.ID
    
    def available_space(self): #method to update the list of available parking spaces and when a vehicle exits the parking lot, the parking space ID is added back to the list
        vehicle.spaces = self.parking_space_ID()[1]
        if self.choice == 2:
            bisect.insort(vehicle.spaces, self.ID)
            return vehicle.spaces
        else:
            return vehicle.spaces
    
    def entry_time(self): #method to record entry time
        if self.enter is None:
            self.enter = time.time()
            return self.enter
        else:
            return self.enter
    
    def entry_time_print(self): #method to print entry time in a readable format
        return time.ctime(self.entry_time())
    
    def exit_time(self): #method to record exit time and to update the timestamp when a vehicle exits the parking lot
        if self.choice == 2:
            self.exit = time.time()
            self.update_timestamp(self.exit)
            return self.exit
        else:
            return self.exit
    
    def exit_time_print(self): #method to print exit time in a readable format
        if self.exit_time() is None:
            return "The vehicle is still inside the parking lot."
        else:
            return time.ctime(self.exit_time())

    #method to check if a vehicle has exited the parking lot. This is used to prevent a vehicle from entering the parking lot twice and it is also used in other exception handling cases    
    def exit_status(self): 
        if self.exit is None:
            return False
        else:
            return True
    
    def fee(self): #method for calculating parking fee
        rate = 2
        if self.exit_time() is None:
            return "Fee will be determined at exit."
        else:
            total_time_hr = (self.exit_time() - self.entry_time())/3600
            dues = round(rate * total_time_hr, 2)
            return str(dues) + " £"

csv_filepath = "parking data.csv" #filepath for csv file

#if the csv file exists, the data is read and stored in the dictionary. Note how instances of the vehicle class are created whenever an entry is read from the csv file
if os.path.exists(csv_filepath): 
    with open (csv_filepath, "r") as file:
            read_data = csv.reader(file)
            header = next(read_data, None)
            choice = None
            for row in read_data:
                count += 1
                parking_lot["Vehicle" + str(count)] = vehicle(row[1], count, choice)
                parking_lot["Vehicle" + str(count)].ticket = row[2]
                parking_lot["Vehicle" + str(count)].ID = int(row[3])
                parking_lot["Vehicle" + str(count)].enter = float(row[4])
                exit_csv_value = lambda exit_val: None if exit_val == "" else float(exit_val) #used to convert the empty string in the csv file to None, which then updates the exit status
                parking_lot["Vehicle" + str(count)].exit = exit_csv_value(row[5])
                parking_lot["Vehicle" + str(count)].parking_space_ID()                

def input_choice(): #function to prompt user for choice
    choice_prompt = input(f"\nWelcome to Shaheer's Car Park! You can choose from the following options: \n 1. Enter the car park. \n 2. Exit the "
                              f"car park. \n 3. View the number of available parking spaces. \n 4. Query parking record using your ticket number. "
                              f"\n 5. Quit \n\nPlease enter your choice (1-5): ")
    if choice_prompt.isdigit(): #exception handling for incorrect input from user. Anything other than a number from 1 to 5 will raise an error
        choice_value = int(choice_prompt)
        if choice_value in range(1,6):
            return choice_value
        else:
            raise ValueError("Incorrect input detected. Please enter a number from 1 to 5")                
    else:
        raise TypeError("Incorrect input detected. Please enter a number from 1 to 5")

def input_command(choice): #function to prompt user for input (registration number or ticket number)
    search = (lambda parameter: "the Registration No. of your vehicle. \nThe format is |SSDD SSS| where S represents a letter and D represents a digit" 
              if parameter != 4 else "your Ticket No. to query your parking record. \nThe format is |DDDD SSDD SSS| where S represents a letter and D represents a digit")
    tracker = input("Please enter %s: " % (search(choice)))
    return tracker.upper()

def input_format(choice, var): #function to format the input (registration number or ticket number) to a standardised format and raise exceptions if the input is invalid
    if choice != 4:
        if len(var) == 8 and var[:2].isalpha() and var[2:4].isdigit() and var[4] == " " and var[5:].isalpha(): #SSDD SSS
            return var
        elif len(var) == 7 and var[:2].isalpha() and var[2:4].isdigit() and var[4:].isalpha(): #SSDDSSS
            return f"{var[:4]} {var[4:]}"
        elif len(var) == 9 and var[:2].isalpha() and var[2] == " " and var[3:5].isdigit() and var[5] == " " and var[6:].isalpha(): #SS DD SSS
            formatted_var = var.replace(" ", "", 1)
            return formatted_var
        else:
            raise ValueError(f"Invalid format for Registration No. detected. \nPlease make sure your vehicle has a valid UK registration number. \nThe "
                             f"format is |SSDD SSS| where S represents a letter and D represents a digit.")
    else:
        if (len(var) == 13 and var[:4].isdigit() and var[4] == " " and var[5:7].isalpha() and var[7:9].isdigit() and var[9] == " " and
             var[10:].isalpha()): #DDDD SSDD SSS
            return var
        elif len(var) == 11 and var[:4].isdigit() and var[4:6].isalpha() and var[6:8].isdigit() and var[8:].isalpha(): #DDDDSSDDSSS
            return f"{var[:4]} {var[4:8]} {var[8:]}"
        elif (len(var) == 14 and var[:4].isdigit() and var[4] == " " and var[5:7].isalpha() and var[7] == " " and 
              var[8:10].isdigit() and var[10] == " " and var[11:].isalpha()): #DDDD SS DD SSS
            formatted_var = var.replace(" ", "")
            return f"{formatted_var[:4]} {formatted_var[4:8]} {formatted_var[8:]}"
        else:
            raise ValueError(f"Invalid format for Ticket Number detected. \nPlease make sure you enter the Ticket Number assigned to your vehicle when you "
                             f"entered the parking lot. \nThe format is |DDDD SSDD SSS| where S represents a letter and D represents a digit.")            

def check_entered_vehicle(val): #function to check if a vehicle that is already in the parking lot is trying to enter again, raises exception if so 
    for key, instance in parking_lot.items():
        if val == instance.reg_no:
            raise ValueError("This vehicle has already entered the parking lot.")
        
def check_available_space(parking_lot): #function to check if there are any parking spaces available in the parking lot, raises exception if not
    parked_vehicles = 0
    
    for key, instance in parking_lot.items():
        if instance.exit_status() is False:
            parked_vehicles += 1
    
    if parked_vehicles >= max_spaces:
        raise ValueError("There are no parking spaces available in the parking lot. \nPlease come back later. We apologise for the inconvenience.")
    else:
        return

def track_vehicle(val, choice): #function to track a vehicle in the parking lot using either the registration number or the ticket number, raises exception if the vehicle is not
    vehicle_finder = None
    for key, instance in parking_lot.items():
        if choice == 2:
            if val == instance.reg_no and instance.exit_status() is False:
                vehicle_finder = instance
                return vehicle_finder
            elif val == instance.reg_no and instance.exit_status() is True:
                raise ValueError("This vehicle has already exited the parking lot.")
        elif choice == 4:
            if val == instance.ticket_no():
                vehicle_finder = instance
                return vehicle_finder
    if vehicle_finder is None:
        criteria = lambda parameter: "registration number" if parameter != 4 else "ticket number"
        raise ValueError(f"There is no vehicle in the parking lot with the provided {criteria(choice)}")

#function to write data to csv file. The csv file is overwritten every time the function is called so that the data taht is read from the csv at the start of the program is not duplicated
def file_writer(): 
    with open (csv_filepath, "w", newline = "") as file:
        row1 = ["Serial No.", "Registration No.", "Ticket No.", "Parking Space ID", "Entry Time", "Exit Time"]
        write1 = csv.writer(file)
        write1.writerow(row1)
        for r, instance in parking_lot.items():
            r = [instance.count, instance.reg_no, instance.ticket_no(), instance.return_ID(), instance.entry_time(), instance.exit_time()]
            write2 = csv.writer(file)
            write2.writerow(r)

#function for GUI
def input_command_GUI(choice):
    search = lambda parameter: "the Registration No. of your vehicle" if parameter != 4 else "your Ticket No. to query your parking record"
    return f"Please enter {search(choice)}. \nAfterwards, please press the Return key to proceed."

