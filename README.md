# CarParkSimulator
This project is an Automated Car Parking System built using Python with two interfaces:

- **Command Prompt Version:** A text-based interface that allows users to interact with the parking system through commands.
- **Graphical User Interface (GUI):** A user-friendly Tkinter-based GUI for easier interaction.

The system manages vehicle entries, exits, and queries, and provides information about available parking spaces. It also records and tracks vehicle data in a simulated parking lot.

## Features
- **Vehicle Entry:** Records the vehicle registration number upon entering the parking lot.
- **Vehicle Exit:** Tracks vehicles leaving the parking lot and updates the available spaces.
- **Query Available Spaces:** Displays the number of available parking spaces.
- **Query Parking Record:** Allows users to query parking records by vehicle registration or ticket number.
- **Save Parking Records:** Saves the vehicle data to a CSV file when the user exits the system.

## Requirements
- Python 3.x
- Tkinter (for the GUI version)

## Installation
Clone this repository to your local machine using the following command:
git clone https://github.com/Shaheer-Rehan/CarParkSimulator.git 

## Usage
### Command Prompt Interface
To run the project using the command prompt interface:
1. Navigate to the project directory
cd CarParkSimulator
2. Run the following command:
python cmd_codeV2.py
You will be prompted to choose one of the following options:
- Enter a vehicle
- Exit a vehicle
- Query available spaces
- Query parking record by vehicle or ticket number
- Quit and save records

### Graphical User Interface
To run the project using the GUI:
1. Navigate to the project directory
cd CarParkSimulator
2. Run the following command:
python gui_code.py
This will open a GUI window where you can interact with the different buttons.

## File Descriptions
- **ParkingLot_basecodeV2.py:** Contains the core functionality for the parking system, including error handling and vehicle management.
- **cmd_codeV2.py:** Command prompt-based interface for interacting with the parking system.
- **gui_code.py:** Tkinter-based graphical interface for interacting with the parking system.

## How It Works
1. **Vehicle Entry:** The system checks for available space before allowing vehicle entry. Each vehicle is assigned a unique ticket number upon entry.
2. **Vehicle Exit:** The user inputs the vehicle's registration number, and the system calculates the time spent in the parking lot. The system then returns the charges for parking based on the time spent in the parking lot.
3. **Available Spaces:** The system keeps track of available spaces and displays the count when requested.
4. **Query Parking Record:** The user can input a vehicle's registration or ticket number to retrieve the parking record.
5. **Save Records:** Upon quitting, the system saves the parking data to a CSV file.
