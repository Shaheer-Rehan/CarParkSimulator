import tkinter as tk
from tkinter import font
from ParkingLot_basecodeV2 import *

window = tk.Tk()
window.title("Shaheer's Parking Lot")

for i in range(3): #setting up the grid
    window.columnconfigure(i, weight = 1, minsize = 100)
    window.rowconfigure(i, weight = 1, minsize = 100)

font_size = 12
font_style = font.Font(size=font_size, weight="bold") #font style for the instructions

#creating the frames and labels for the instructions and display widgets
frm_instruct = tk.Frame(master = window, relief = tk.FLAT, borderwidth=2, width = 38, height = 20)
lbl_instruct = tk.Label(master = frm_instruct, text = "Please select one of the following options:", 
                        height = 4, width = 32, borderwidth = 0, font = font_style)
frm_instruct.grid(row = 0, column = 0, columnspan = 3)
lbl_instruct.pack(fill = tk.BOTH, padx = 10, pady = 10)

frm_display = tk.Frame(master = window, relief = tk.GROOVE, borderwidth = 1, height = 30)
lbl_display = tk.Label(master = frm_display, text = "", borderwidth = 2)
frm_display.grid(row = 3, column = 0, columnspan = 5, padx = 10, pady = 50)
lbl_display.pack(fill = tk.BOTH, padx = 10, pady = 10)

lbl_prompt = None
ent_input = None
choice_setter = tk.StringVar()
prompt_text = tk.StringVar()
user_data_retriever = tk.StringVar()
press_return = tk.BooleanVar()

def choice_updater(value): #function to update the choice variable
    choice_setter.set(value)

def update_prompt(): #function to update the prompt text
    choice = int(choice_setter.get())
    prompt_text.set(input_command_GUI(choice))
    return choice

def disable_buttons(): #function to disable the buttons. This is needed to prevent the user from clicking the buttons before hitting the return key after inputting the data
    btn_enter.config(state=tk.DISABLED)
    btn_exit.config(state=tk.DISABLED)
    btn_space.config(state=tk.DISABLED)
    btn_query.config(state=tk.DISABLED)
    btn_quit.config(state=tk.DISABLED)

def enable_buttons(): #function to enable the buttons back again
    btn_enter.config(state=tk.NORMAL)
    btn_exit.config(state=tk.NORMAL)
    btn_space.config(state=tk.NORMAL)
    btn_query.config(state=tk.NORMAL)
    btn_quit.config(state=tk.NORMAL)

def get_user_data(event, ent_input): #function to get the user data from the entry widget
    user_data_retriever.set(ent_input.get())
    press_return.set(True)
    enable_buttons()

def widget_cleaner(): #function to clean up the prompt and input widgets for when they are not needed
    global lbl_prompt, ent_input
    if lbl_prompt is not None:
        lbl_prompt.destroy()
    if ent_input is not None and ent_input.winfo_exists():
        ent_input.unbind("<Return>") #unbinding the event handler
        ent_input.destroy()

def input_widgets(): #function to create the prompt and input widgets and receive the user data and return it
    global lbl_prompt, ent_input
    widget_cleaner()

    frm_prompt = tk.Frame(master = window, relief = tk.FLAT, borderwidth = 0)
    lbl_prompt = tk.Label(master = frm_prompt, textvariable = prompt_text, borderwidth = 0)
    frm_prompt.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = "e")
    lbl_prompt.pack(fill = tk.BOTH, padx = 5, pady = 5)

    frm_input = tk.Frame(master = window, relief = tk.FLAT, borderwidth = 0)
    ent_input = tk.Entry(master = frm_input, width = 16, borderwidth = 2)
    frm_input.grid(row = 2, column = 3, padx = 5, pady = 5, sticky = "w")
    ent_input.pack(fill = tk.BOTH, padx = 5, pady = 5)
    
    press_return.set(False)
    ent_input.bind("<Return>", lambda event: get_user_data(event, ent_input))
    window.wait_variable(press_return)
    user_data = (user_data_retriever.get()).upper()
    
    return user_data

def close_window(): #function to close the window after the quit button or the "X" button is pressed
    for widget in window.winfo_children():
        widget.destroy()
    
    frm_close = tk.Frame(master = window, relief = tk.SUNKEN, borderwidth = 3)
    lbl_close = tk.Label(master = frm_close, text = "", font = 14, borderwidth = 0)
    lbl_close["text"] = str("Thank you for choosing Shaheer's Car Park. Have a safe journey! \n\nThis window will self-destruct in 5 seconds.")
    frm_close.grid(row = 1, column = 1, padx = 10, pady = 50)
    lbl_close.pack(fill = tk.BOTH, padx = 10, pady = 10)
    window.update()
    time.sleep(8) #factoring in time for user to read the message
    window.destroy()

def btn_response(value): #function to respond to the button presses. The code in this block is similar to the one in cmd_codeV2.py
    choice_updater(value)
    choice = update_prompt()
    
    if choice == 1:
        try: #try-except block for when the parking lot is full. This is needed to prevent the program from crashing 
            check_available_space(parking_lot)
        except ValueError as err:
            widget_cleaner()
            lbl_display["text"] = str("Error: " + str(err))
            return 
        
        disable_buttons() #disabling the buttons to prevent the user from clicking them before hitting the return key after inputting the data
        lbl_display["text"] = "" #clearing the display label to prevent the previous output from being displayed
        try:
            global count
            user_data = input_widgets()         
            reginum = input_format(choice, user_data)
            check_entered_vehicle(reginum)
            count += 1
            parking_lot["Vehicle" + str(count)] = vehicle(reginum, count, choice) 
            lbl_display["text"] = str(parking_lot["Vehicle" + str(count)])
        except ValueError as err:
            lbl_display["text"] = str("Error: " + str(err))

    elif choice == 2:
        disable_buttons()
        lbl_display["text"] = ""
        try:
            user_data = input_widgets()
            reginum = input_format(choice, user_data)
            vehicle_tracker = track_vehicle(reginum, choice)
            vehicle_tracker.choice = choice
            lbl_display["text"] = str(vehicle_tracker)
        except ValueError as err:
            lbl_display["text"] = str("Error: " + str(err))
    
    elif choice == 3:
        widget_cleaner()
        lbl_display["text"] = ""
        vehicle_tracker = None
        if parking_lot == {}: #if the parking lot is empty
            lbl_display["text"] = str("The number of spaces available inside the parking lot is 8")
        else:
            vehicle_tracker = max(parking_lot.values(), key = lambda find: find.timestamp)
            vehicle_tracker.choice = choice
            lbl_display["text"] = str("The number of spaces available inside the parking lot is " + str(len(vehicle_tracker.available_space())))
        
    elif choice == 4:
        disable_buttons()
        lbl_display["text"] = ""
        try:
            user_data = input_widgets()
            ticket_search = input_format(choice, user_data)
            vehicle_tracker = track_vehicle(ticket_search, choice)
            vehicle_tracker.choice = choice
            lbl_display["text"] = str(vehicle_tracker)
        except ValueError as err:
            lbl_display["text"] = str("Error: " + str(err))

    elif choice == 5:
        lbl_display["text"] = ""
        file_writer()
        close_window()

#creating the buttons and frames for the buttons
frm_enter = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 5, 
                     width = 18, height = 10)
btn_enter = tk.Button(master = frm_enter, text = "Enter", height = 4, width = 12,
                      command = lambda: btn_response(1))
frm_enter.grid(row = 1, column = 0, padx = 10, pady = 10)
btn_enter.pack(fill = tk.BOTH, padx = 10, pady = 10)

frm_exit = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 5, 
                     width = 18, height = 10)
btn_exit = tk.Button(master = frm_exit, text = "Exit", height = 4, width = 12,
                     command = lambda: btn_response(2))
frm_exit.grid(row = 1, column = 1, padx = 10, pady = 10)
btn_exit.pack(fill = tk.BOTH, padx = 10, pady = 10)

frm_space = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 5, 
                     width = 18, height = 10)
btn_space = tk.Button(master = frm_space, text = "Available \nSpaces", 
                      height = 4, width = 12, command = lambda: btn_response(3))
frm_space.grid(row = 1, column = 2, padx = 10, pady = 10)
btn_space.pack(fill = tk.BOTH, padx = 10, pady = 10)

frm_query = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 5, 
                     width = 18, height = 10)
btn_query = tk.Button(master = frm_query, text = "Query \nParking Record", 
                      height = 4, width = 12, command = lambda: btn_response(4))
frm_query.grid(row = 1, column = 3, padx = 10, pady = 10)
btn_query.pack(fill = tk.BOTH, padx = 10, pady = 10)

frm_quit = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 5, 
                     width = 18, height = 10)
btn_quit = tk.Button(master = frm_quit, text = "Quit", height = 4, width = 12, 
                     command = lambda: btn_response(5))
frm_quit.grid(row = 1, column = 4, padx = 10, pady = 10)
btn_quit.pack(fill = tk.BOTH, padx = 10, pady = 10)

def direct_close(): #function to close the window and save data to csv when the "X" button is pressed
    btn_response(5)

window.protocol("WM_DELETE_WINDOW", direct_close) #binding the function to the "X" button

window.mainloop()