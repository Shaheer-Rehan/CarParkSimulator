from ParkingLot_basecodeV2 import *

take_input = True
while take_input:
    try: #try-except block to catch any errors. All errors are defined in the base code
        choice = input_choice()
        if choice == 1:
            try:
                check_available_space(parking_lot)
                user_data = input_command(choice)
                reginum = input_format(choice, user_data)
                check_entered_vehicle(reginum)
                count += 1
                parking_lot["Vehicle" + str(count)] = vehicle(reginum, count, choice)
                print(parking_lot["Vehicle" + str(count)])
            except ValueError as err:
                print("Error: " + str(err))

        elif choice == 2:
            try:
                user_data = input_command(choice)
                reginum = input_format(choice, user_data)
                vehicle_tracker = track_vehicle(reginum, choice)
                vehicle_tracker.choice = choice
                print(vehicle_tracker)
            except ValueError as err:
                print("Error: " + str(err))
            
        elif choice == 3: 
            vehicle_tracker = None
            if parking_lot == {}: #if the parking lot is empty
                print("The number of spaces available inside the parking lot is 8")
            else:
                vehicle_tracker = max(parking_lot.values(), key = lambda find: find.timestamp)
                vehicle_tracker.choice = choice
                print("The number of spaces available inside the parking lot is " + str(len(vehicle_tracker.available_space())))
            
        elif choice == 4:
            try:
                user_data = input_command(choice)
                ticket_search = input_format(choice, user_data)
                vehicle_tracker = track_vehicle(ticket_search, choice)
                vehicle_tracker.choice = choice
                print(vehicle_tracker)
            except ValueError as err:
                print("Error: " + str(err))
            
        elif choice == 5:
            file_writer()
            take_input = False
            print("Thank you for choosing Shaheer's Car Park. Have a safe journey!")
    
    except Exception as err:
        print("Error: " + str(err))
