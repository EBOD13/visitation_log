import customtkinter as ctk
from customtkinter import CTkToplevel
from twilio.rest import Client
from CTkMessagebox import CTkMessagebox
import re
import tkinter
import json
from datetime import datetime
import secrets # File contains all API keys and auth from Twilio and the WeatherAPI
import sys
import os
from weather import WeatherDisplayFrame


class App(ctk.CTk):
    def __init__(self, **kwargs):
        """
       Initialize the main application window.

       Parameters:
       - **kwargs: Additional keyword arguments.

       This constructor sets up the main application window with specific attributes.
       """
        super().__init__(**kwargs)

        def icon_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        icon_path = icon_path(r"data\Headington Logo.ico")

        self.geometry("500x700")  # Set the initial window size
        self.iconbitmap(icon_path)  # Set the window icon
        self.title("Headington Portal")  # Set the window title
        self.resizable(False, False)  # Disable window resizing
        self.main_screen = MainScreen(self, self.winfo_screenheight(),
                                      self.winfo_screenwidth())  # Create the main screen
        self.current_screen = None  # Track the current active screen

        self.show_main_screen()  # Show the main screen initially

    def show_main_screen(self):
        """
        Display the main screen.

        This function hides the current screen, if any, and displays the main screen.
        """
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.main_screen.pack(fill='both', expand=True)  # Display the main screen
        self.current_screen = self.main_screen  # Update the current active screen


class MainScreen(ctk.CTkFrame):

    def __init__(self, container, app_height, app_width):
        """
        Initialize the main screen.

        Parameters:
        - container: The parent container.
        - app_height: Height of the application window.
        - app_width: Width of the application window.

        This constructor sets up the main screen with various widgets.
        """
        super().__init__(container, height=app_height, width=app_width)

        # Create and place widgets on the main screen
        new_entry_label = ctk.CTkLabel(self, text="New Entry", font=("Times", 18, "bold"))
        new_entry_label.place(relx=0.03, rely=0.03)
        res_combobox = ctk.CTkComboBox(self, width=200, values=None, variable=None, state='disabled')
        res_combobox.place(relx=0.03, rely=0.25)
        vis_combobox = ctk.CTkComboBox(self, values=None, variable=None, width=200, state="disabled")
        vis_combobox.place(relx=0.55, rely=0.25)
        checkout_button = ctk.CTkButton(self, text="Check Out", width=95, fg_color="#841617",
                                        hover_color='#991112')
        checkout_button.place(relx=0.24, rely=0.94)

        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """

            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        visitation_path = resource_path(r"data\visitation_log.json")
        people_path = resource_path(r"data\people_profile.json")

        # Several functions for widget behavior and states
        # Function to capitalize entries and make change email to lowercase
        def caps(event):
            fname_input.set(fname_input.get().title())
            lname_input.set(lname_input.get().title())
            room_input.set(room_input.get().title())
            mail_input.set(mail_input.get().lower())
            vis_fname_input.set(vis_fname_input.get().title())
            vis_lname_input.set(vis_lname_input.get().title())

        # Function to limit the res_room entry to a length of 4
        def validate_input(phone_number):
            # phone_number is the proposed input; return True to allow, False to reject
            return phone_number.isdigit() and len(phone_number) <= 10 or phone_number == ""

        # Register validation function and event handlers
        validate_func = self.register(validate_input)

        def set_entry_limit(room):
            if len(room_input.get()) > 0:
                room_input.set(room_input.get()[:4])

        # Function to change the states of the widgets
        # Default state: All input fields are enabled
        def change_state(states):
            if states == 'DR':
                res_fname_entry.configure(state="readonly")
                res_lname_entry.configure(state="readonly")
                res_email_entry.configure(state="readonly")
            elif states == 'DV':
                vis_fname_entry.configure(state="readonly")
                vis_lname_entry.configure(state="readonly")
                vis_cont_entry.configure(state="readonly")
                checkin_time.configure(state="readonly")
                date_entry.configure(state="readonly")
            elif states == "ER":
                res_fname_entry.configure(state="normal")
                res_lname_entry.configure(state="normal")
                res_email_entry.configure(state="normal")
            elif states == "EV":
                vis_fname_entry.configure(state="normal")
                vis_lname_entry.configure(state="normal")
                vis_cont_entry.configure(state="normal")
                checkin_time.configure(state="normal")
                date_entry.configure(state="normal")
            elif states == "E_ALL":
                res_fname_entry.configure(state="normal")
                res_lname_entry.configure(state="normal")
                res_email_entry.configure(state="normal")
                vis_fname_entry.configure(state="normal")
                vis_lname_entry.configure(state="normal")
                vis_cont_entry.configure(state="normal")
                checkin_time.configure(state="normal")
                date_entry.configure(state="normal")
            elif states == "R_ALL":
                res_fname_entry.configure(state="readonly")
                res_lname_entry.configure(state="readonly")
                res_email_entry.configure(state="readonly")
                vis_fname_entry.configure(state="readonly")
                vis_lname_entry.configure(state="readonly")
                vis_cont_entry.configure(state="readonly")
                checkin_time.configure(state="readonly")
                date_entry.configure(state="readonly")

            elif states == "D_ALL":
                res_fname_entry.configure(state="disabled")
                res_lname_entry.configure(state="disabled")
                res_email_entry.configure(state="disabled")
                vis_fname_entry.configure(state="disabled")
                vis_lname_entry.configure(state="disabled")
                vis_cont_entry.configure(state="disabled")
                checkin_time.configure(state="disabled")
                date_entry.configure(state="disabled")
            else:
                pass

        # Function to clear all the widgets' entries
        def clear(field):
            """
            Clear specific entry fields and update combo box states.

            Args:
                field (str): The field to be cleared. Options: 'all', 'res_all', 'res', 'vis', 'd_all'.

            Returns:
                None
            """
            change_state("E_ALL")  # Reset all entry widgets to normal state

            if field in ("all", "res_all"):
                widgets_to_clear = [res_fname_entry, res_lname_entry, res_email_entry, res_room_entry, vis_fname_entry,
                                    vis_lname_entry, vis_cont_entry, checkin_time, date_entry]
            elif field == "res":
                widgets_to_clear = [res_fname_entry, res_lname_entry, res_email_entry]

            elif field == "vis":
                widgets_to_clear = [vis_fname_entry, vis_lname_entry, vis_cont_entry, checkin_time, date_entry]
            elif field == "d_all":
                widgets_to_clear = [res_fname_entry, res_lname_entry, res_email_entry, res_room_entry, vis_fname_entry,
                                    vis_lname_entry, vis_cont_entry, checkin_time, date_entry]
                vis_combobox.set("")
                res_combobox.set("")
                vis_combobox.configure(state="disabled")
                res_combobox.configure(state="disabled")
            else:
                return  # Handle other cases or raise an exception if needed

            for widget in widgets_to_clear:
                widget.delete(0, tkinter.END)

        # Labels for the Entry boxes
        # Labels for Entry Boxes
        search_room_label = ctk.CTkLabel(self, text="Search by Room:",
                                         font=("Times", 15))  # Label for searching by room
        res_label = ctk.CTkLabel(self, text="Visitor Information",
                                 font=("Times", 20, "bold", "italic"))  # Label for visitor information
        res_fname_label = ctk.CTkLabel(self, text="First Name:", font=("Times", 14))  # Label for resident first name
        res_lname_label = ctk.CTkLabel(self, text="Last Name:", font=("Times", 14))  # Label for resident last name
        res_mail_label = ctk.CTkLabel(self, text="Email:", font=("Times", 14))  # Label for resident email
        vis_fname_label = ctk.CTkLabel(self, text="First Name:", font=("Times", 14))  # Label for visitor first name
        vis_lname_label = ctk.CTkLabel(self, text="Last Name:", font=("Times", 14))  # Label for visitor last name
        vis_cont_label = ctk.CTkLabel(self, text="Phone number:", font=("Times", 14))  # Label for visitor phone number

        # Placing Labels for Entry Boxes
        search_room_label.place(relx=0.03, rely=0.15)
        res_label.place(relx=0.55, rely=0.18)
        res_fname_label.place(relx=0.03, rely=0.3)
        res_lname_label.place(relx=0.03, rely=0.4)
        res_mail_label.place(relx=0.03, rely=0.5)
        vis_fname_label.place(relx=0.55, rely=0.3)
        vis_lname_label.place(relx=0.55, rely=0.4)
        vis_cont_label.place(relx=0.55, rely=0.5)

        # Using StringVar to store the String Variable of the Entry field - which I used above to format them as Title
        fname_input = tkinter.StringVar()
        lname_input = tkinter.StringVar()
        room_input = tkinter.StringVar()
        mail_input = tkinter.StringVar()
        vis_fname_input = tkinter.StringVar()
        vis_lname_input = tkinter.StringVar()
        vis_cont_input = tkinter.StringVar()

        # Creating the customtkinter entry boxes
        # Resident
        res_room_entry = ctk.CTkEntry(self, font=("Times", 14), width=90,
                                      textvariable=room_input)  # Entry for resident room
        res_fname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=fname_input,
                                       width=200)  # Entry for resident first name
        res_lname_entry = ctk.CTkEntry(self, font=("Times", 14), width=200,
                                       textvariable=lname_input)  # Entry for resident last name
        res_email_entry = ctk.CTkEntry(self, font=("Times", 14), width=200,
                                       textvariable=mail_input)  # Entry for resident email
        # Visitors
        vis_fname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=vis_fname_input,
                                       width=200)  # Entry for visitor first name
        vis_lname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=vis_lname_input,
                                       width=200)  # Entry for visitor last name
        vis_cont_entry = ctk.CTkEntry(self, validate="key",
                                      validatecommand=(validate_func, "%P"))  # Entry for visitor phone number
        now_day = ctk.StringVar()
        now_day.set(datetime.today().strftime("%m/%d/%y"))
        date_entry = ctk.CTkEntry(self, font=("Times", 14), width=67, textvariable=now_day)
        checkin_time = ctk.CTkEntry(self, font=("Times", 14), width=50)
        # checkout_time = ctk.CTkEntry(self, font=("Times", 14), width=50)

        # Placing all my entry boxes - in order
        # Resident
        res_room_entry.place(relx=0.25, rely=0.15)
        res_fname_entry.place(relx=0.03, rely=0.35)
        res_lname_entry.place(relx=0.03, rely=0.45)
        res_email_entry.place(relx=0.03, rely=0.55)
        # Visitors
        vis_fname_entry.place(relx=0.55, rely=0.35)
        vis_lname_entry.place(relx=0.55, rely=0.45)
        vis_cont_entry.place(relx=0.55, rely=0.55)

        # Formatting the entries into Title (First letter is capital)
        # Resident
        res_room_entry.bind("<KeyRelease>", caps)
        res_fname_entry.bind("<KeyRelease>", caps)
        res_lname_entry.bind("<KeyRelease>", caps)
        res_email_entry.bind("<KeyRelease>", caps)
        room_input.trace("w", lambda *args: set_entry_limit(room_input))
        # Visitors
        vis_fname_entry.bind("<KeyRelease>", caps)
        vis_lname_entry.bind("<KeyRelease>", caps)
        vis_cont_entry.bind("<KeyRelease>", caps)

        vis_cout_combobox = ctk.CTkComboBox(self, values=None, variable=ctk.StringVar(value="No Visitor"), width=200,
                                            state="disabled")

        def add_resident(res_fname, res_lname, res_email, res_room, filename=people_path):
            """
            Add a resident to the system.

            Args:
                res_fname (str): The resident's first name.
                res_lname (str): The resident's last name.
                res_email (str): The resident's email.
                res_room (str): The resident's room number.
                filename (str, optional): The file to save the resident data. Defaults to people_path.
            """
            res_room = str(re.findall("[A-Za-z]\\d{3}", res_room)[0])
            full_name = res_fname.lower() + " " + res_lname.lower()
            resident_profile = {"full_name": full_name.strip(),
                                "email": res_email.lower().strip(),
                                "room": res_room.lower().strip(),
                                "visitors": []
                                }
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                # Checks if there is no resident, this creates a new one. If there is no resident with the given data,
                # the new data create a resident
                if not bool(file_data['residents']):
                    # If there are no residents, create a new one.
                    file_data['residents'].append(resident_profile)
                    file.seek(0)
                    json.dump(file_data, file, indent=1)
                elif all(file_data.get('residents')) and not any(
                        resident.get('full_name', '').lower() == full_name.lower() for resident in
                        file_data.get('residents', [])):
                    # If residents exist but no matching resident, create a new one.
                    file_data['residents'].append(resident_profile)
                    file.seek(0)
                    json.dump(file_data, file, indent=1)

        def fill_visitor_entries(choice):
            """
           Fill visitor entry fields with data based on the selected visitor choice.

           Args:
               choice (str): The selected visitor's name.

           Returns:
               str: The selected visitor's full name.
           """
            time_now = datetime.now().strftime("%H:%M")
            today = datetime.today().strftime("%m/%d/%y")
            clear("vis")

            checkin_time.insert(0, time_now)
            date_entry.insert(0, today)
            vis_fname_entry.insert(0, choice.split(" ")[0])
            vis_lname_entry.insert(0, choice.split(" ")[1])

            for i in range(len(make_visitor_list()[1])):
                if choice.split(" ")[0] == make_visitor_list()[1][i].split(" ")[0] and choice.split(" ")[1] == \
                        make_visitor_list()[1][i].split(" ")[1]:
                    vis_cont_entry.configure(state="normal")
                    vis_cont_entry.insert(0, make_visitor_list()[1][i].split(" ")[2])
            vis_fname_entry.configure(state="readonly")
            change_state("R_ALL")
            return choice.split(" ")[0] + " " + choice.split(" ")[1]

        def fill_resident_entries(choice):
            """
            Fill resident entry fields with data based on the selected resident choice.

            Args:
                choice (str): The selected resident's name.

            Returns:
                str: The selected resident's full name.
            """
            clear("res")

            res_fname_entry.insert(0, choice.split(" ")[0])
            res_lname_entry.insert(0, choice.split(" ")[1])

            for i in range(len(make_resident_list()[1])):
                if choice.split(" ")[0] == make_resident_list()[1][i].split(" ")[0] and choice.split(" ")[1] == \
                        make_resident_list()[1][i].split(" ")[1]:
                    res_email_entry.configure(state="normal")
                    res_email_entry.delete(0, tkinter.END)
                    res_email_entry.insert(0, make_resident_list()[1][i].split(" ")[2])

            # Clear previously filled visitor entries
            clear("vis")

            # Explicitly clear the date_entry field
            date_entry.configure(state="normal")
            date_entry.delete(0, tkinter.END)

            # Update the visitor list and set the values for vis_combobox
            list_of_visitors, _ = make_visitor_list()
            if len(list_of_visitors) == 0:
                vis_combobox_var = ctk.StringVar(value="Select Visitor")
            else:
                vis_combobox_var = ctk.StringVar(value=list_of_visitors[0])

            vis_combobox.configure(state="readonly", variable=vis_combobox_var, values=list_of_visitors,
                                   command=fill_visitor_entries)

            change_state("DR")

            return choice.split(" ")[0] + " " + choice.split(" ")[1]

        def make_resident_list(event=None, filename=people_path):
            """
            Create a list of residents based on the specified room and update the res_combobox.

            Args:
                event (Event, optional): Event that triggered the update. Defaults to None.
                filename (str, optional): The file containing resident data. Defaults to people_path.

            Returns:
                list: A list of residents and their emails.
            """
            res_room = res_room_entry.get().strip()  # Ensure you have a valid res_room_entry
            with open(filename, 'r+') as file:
                file_data = json.load(file)

            # Create a list to store resident names and emails
            list_of_residents = []
            list_of_resMails = []

            # Collect resident names
            for resident in file_data['residents']:
                if resident['room'].lower() == res_room.lower():
                    # Append resident's full name to the list with their respective emails
                    list_of_residents.append(resident.get('full_name').title())
                    list_of_resMails.append(resident.get('full_name').title() + " " + resident.get('email').lower())

            # Create the res_combobox and set its values
            if len(list_of_residents) > 0:
                res_combobox_var = ctk.StringVar(value=list_of_residents[0])
            else:
                clear("res")
                # Handle the case when no residents are found
                res_combobox_var = ctk.StringVar(value="No Residents Found")

            res_combobox.configure(values=list_of_residents, variable=res_combobox_var, width=200,
                                   command=fill_resident_entries, state="readonly")

            def update_visitor_list(event=None):
                # Only update the visitor list if both res_fname_entry and res_combobox have valid values
                if res_combobox.get() == "No Residents Found":
                    make_visitor_list()

            update_visitor_list()

            return [list_of_residents, list_of_resMails]

        def make_visitor_list(event=None, filename=people_path):
            """
           Create a list of visitors for the selected resident and update the vis_combobox.

           Args:
               event (Event, optional): Event that triggered the update. Defaults to None.
               filename (str, optional): The file containing resident data. Defaults to people_path.

           Returns:
               list: A list of visitors and their contacts.
           """
            res_fname = res_fname_entry.get()
            res_lname = res_lname_entry.get()
            full_name = f"{res_fname.lower()} {res_lname.lower()}"

            with open(filename, 'r+') as file:
                file_data = json.load(file)

            # Create a list to store visitor names
            list_of_visitors = []
            list_of_mails = []

            # Collect visitor names
            for resident in file_data['residents']:
                if resident['full_name'].lower().strip() == full_name.lower().strip():
                    for visitor in resident["visitors"]:
                        # Append visitor's full name to the list
                        list_of_visitors.append(visitor.get('vis_fullname').title())
                        list_of_mails.append(
                            visitor.get('vis_fullname').title() + " " + visitor.get('vis_cont').lower())

            if len(list_of_visitors) > 0:
                vis_combobox_var = ctk.StringVar(value=list_of_visitors[0])
            else:
                clear("vis")

                vis_combobox_var = ctk.StringVar(value="No visitor found")

            vis_combobox.configure(state="readonly", variable=vis_combobox_var, values=list_of_visitors,
                                   command=fill_visitor_entries)
            return [list_of_visitors, list_of_mails]

        # Bind the make_visitor_list function to changes in the res_fname_entry
        # if res_room_entry.get()
        # res_fname_entry.bind("<KeyRelease>", make_visitor_list)

        # Button to clear everything and disable the comboboxes
        clear_button = ctk.CTkButton(self, text="Delete", font=("Times", 14), width=200, )
        clear_button.bind("<Button-1>", lambda event: clear("d_all"))
        clear_button.place(relx=0.03, rely=0.625)

        def add_visitor(vis_fname, vis_lname, vis_cont, res_room, res_name, filename=people_path):
            """
            Add a visitor to the selected resident's visitors list.

            Args:
                vis_fname (str): Visitor's first name.
                vis_lname (str): Visitor's last name.
                vis_cont (str): Visitor's contact information.
                res_room (str): The resident's room number.
                res_name (str): The full name of the resident.
                filename (str, optional): The file containing resident data. Defaults to people_path.
            """
            vis_full_name = f"{vis_fname.lower()} {vis_lname.lower()}"
            visitor_profile = {"vis_fullname": vis_full_name, "vis_cont": vis_cont}

            with open(filename, 'r+') as file:
                file_data = json.load(file)

                for resident in file_data['residents']:
                    if len(resident["visitors"]) == 0 and resident['full_name'].lower() == res_name.lower() and \
                            resident['room'].lower() == res_room.lower():
                        resident['visitors'].append(visitor_profile)
                        file.seek(0)
                        json.dump(file_data, file, indent=1)
                    elif len(resident["visitors"]) > 0 and resident['full_name'].lower() == res_name.lower() and \
                            resident['room'].lower() == res_room.lower():
                        # Create a list of unique full names and emails already in the resident's visitors list
                        existing_names = {v['vis_fullname'] for v in resident['visitors']}
                        existing_emails = {v['vis_cont'] for v in resident['visitors']}
                        # Check if the new visitor's full name and email are not in the existing set
                        if vis_full_name.lower() not in existing_names or vis_cont.lower() not in existing_emails:
                            resident['visitors'].append(visitor_profile)
                            file.seek(0)
                            json.dump(file_data, file, indent=1)

        def checkin_visitor(vis_fname, vis_lname, vis_cont, res_room, res_name, filename=visitation_path):
            """
           Check in a visitor and record their information.

           Args:
               vis_fname (str): Visitor's first name.
               vis_lname (str): Visitor's last name.
               vis_cont (str): Visitor's contact information.
               res_room (str): The resident's room number.
               res_name (str): The full name of the resident.
               filename (str, optional): The file containing visitation data. Defaults to visitation_path.

           Returns:
               bool: True if the visitor is already checked in for the current date, False otherwise.
           """
            time_now = datetime.now().strftime('%H:%M')
            checkin_date = datetime.today().strftime('%m/%d/%y')
            vis_full_name = f'{vis_fname.lower()} {vis_lname.lower()}'
            visitor_profile = {
                'checkin_date': checkin_date,
                'res_fullname': res_name,
                'vis_fullname': vis_full_name,
                'res_room': res_room,
                'vis_cont': vis_cont,
                'checkin_time': time_now,
                'checkout_time': ''
            }

            # Load existing visitation data
            with open(filename, 'r') as file:
                file_data = json.load(file)

            # Check if the visitor is already checked in for the current date
            for visit in file_data['visitation']:
                if visit['checkin_date'] == checkin_date and visit['checkout_time'] == '':
                    if visit['vis_fullname'].lower() == vis_full_name:
                        msg = CTkMessagebox(title="Warning", message="Visitor already checked-in"
                                            , icon="cancel",
                                            option_1="OK")
                        return True

            else:
                # Add the new visitor to the list
                file_data['visitation'].append(visitor_profile)

                # Save the updated visitation data
                with open(filename, 'w') as file:
                    json.dump(file_data, file, indent=4)
                    msg = CTkMessagebox(title="Success", message="Visitor successfully "
                                                                 f"checked-in. \n"
                                                                 f"Date: {checkin_date} \nTime: {time_now} "
                                        , icon="check",
                                        option_1="OK")
                return False

        def validate_entry(event=None):
            """
            Validate visitor and resident information and check in the visitor.

            Args:
                event (Event, optional): The event that triggered the validation. Defaults to None.
            """

            resident_room = res_room_entry.get().lower().strip()
            resident_room_pattern = "^[A-Za-z]\d{3}"  # The desired pattern
            checkin_times = datetime.now().strftime("%H:%M")
            checkin_date = datetime.today().strftime("%m/%d/%y")

            if re.match(resident_room_pattern, resident_room):
                resident_full_name = f"{res_fname_entry.get().lower().strip()} {res_lname_entry.get().lower().strip()}"
                visitor_full_name = f"{vis_fname_entry.get().lower().strip()} {vis_lname_entry.get().lower().strip()}"

                all_conditions_met = (
                        res_fname_entry.get() and
                        res_lname_entry.get() and
                        resident_room and
                        vis_fname_entry.get() and
                        vis_lname_entry.get()
                )
                if all_conditions_met:
                    found_resident = False
                    found_visitor = False
                    with open(people_path, 'r+') as file:
                        file_data = json.load(file)
                        for resident in file_data["residents"]:
                            if resident['full_name'].lower() == resident_full_name.lower().strip():
                                found_resident = True
                                for visitor in resident["visitors"]:
                                    if visitor["vis_fullname"] == visitor_full_name.lower().strip():
                                        found_visitor = True
                                        try:
                                            checkin_visitor(vis_fname_entry.get().strip(), vis_lname_entry.get().strip()
                                                            , vis_cont_entry.get().strip(), resident_room.strip(),
                                                            resident_full_name.strip())

                                        # Update the vis_combobox with no visitors found
                                        except json.JSONDecodeError:
                                            msg = CTkMessagebox(title="Error", message="Error: Submission unsuccessful."
                                                                , icon="cancel",
                                                                option_1="OK")
                                        break

                        if found_resident and not found_visitor:
                            add_visitor(vis_fname_entry.get().strip(), vis_lname_entry.get().strip(),
                                        vis_cont_entry.get().strip(),
                                        res_room_entry.get().strip(), resident_full_name.strip())
                            checkin_visitor(vis_fname_entry.get().strip(), vis_lname_entry.get().strip(),
                                            vis_cont_entry.get().strip(),
                                            resident_room.strip(), resident_full_name.strip())
                            msg = CTkMessagebox(title="Success", message=f"New visitor successfully added\n"
                                                                         f"Date: {checkin_date} \nTime: {checkin_times}",
                                                icon="check", option_1="OK")

                        elif not found_resident and not found_visitor:
                            add_resident(res_fname_entry.get().strip(), res_lname_entry.get().strip(),
                                         res_email_entry.get().strip(), resident_room.strip())
                            add_visitor(vis_fname_entry.get().strip(), vis_lname_entry.get().strip(),
                                        vis_cont_entry.get().strip(),
                                        res_room_entry.get().strip(), resident_full_name.strip())
                            checkin_visitor(vis_fname_entry.get().strip(), vis_lname_entry.get().strip(),
                                            vis_cont_entry.get().strip(),
                                            resident_room.strip(), resident_full_name.strip())
                            msg = CTkMessagebox(title="Success", message=f"Resident and visitor successfully checked-in"
                                                                         f"\nDate:{checkin_date} \nTime: {checkin_times}"
                                                , icon="check",
                                                option_1="OK")
                    clear("all")
                    vis_combobox.set("")
                    res_combobox.set("")
                    vis_combobox.configure(state="disabled")
                    res_combobox.configure(state="disabled")
                    # change_state("D_ALL")
                    checkout_visitors_list()
                else:
                    msg = CTkMessagebox(title="Warning", message="Kindly complete all required fields.", icon="warning",
                                        option_1="OK")
            else:
                msg = CTkMessagebox(title="Warning", message="Kindly complete all required fields.", icon="warning",
                                    option_1="OK")

        res_room_entry.bind("<KeyRelease>", make_resident_list)
        submit_button = ctk.CTkButton(self, text="Submit Entry", font=("Times", 14), width=200, fg_color="#841617",
                                      hover_color='#991112')
        submit_button.bind("<Button-1>", validate_entry)
        submit_button.place(relx=0.55, rely=0.625)

        # Check out visitor section
        checkout_label = ctk.CTkLabel(self, text="Check-out Visitor", font=("Times", 16, "bold"))
        checkout_label.place(relx=0.03, rely=0.69)
        vis_cout_combobox.place(relx=0.03, rely=0.74)
        vis_cout_fname = ctk.CTkEntry(self, width=200)
        vis_cout_lname = ctk.CTkEntry(self, width=200)
        vis_cout_fname.place(relx=0.03, rely=0.81)
        vis_cout_lname.place(relx=0.03, rely=0.88)

        # Function to change the state of the Visitor to check out entry fields
        def change_cout_state():
            """
            Change the state of the checkout visitor entry fields to 'readonly'.
            """
            vis_cout_fname.configure(state="readonly")
            vis_cout_lname.configure(state="readonly")

        def checkout_visitor_entries(choice):
            """
            Fill the checkout visitor entry fields with the selected visitor's information.

            Args:
                choice (str): The selected visitor's name.

            Returns:
                str: The full name of the selected visitor.
            """
            vis_cout_fname.configure(state="normal")
            vis_cout_lname.configure(state="normal")

            vis_cout_fname.delete(0, tkinter.END)
            vis_cout_lname.delete(0, tkinter.END)

            vis_fname, vis_lname = choice.split(" ")
            vis_cout_fname.insert(0, vis_fname)
            vis_cout_lname.insert(0, vis_lname)

            vis_cout_fname.configure(state="readonly")
            vis_cout_lname.configure(state="readonly")

            return vis_fname + " " + vis_lname

        def checkout_visitors_list(event=None):
            """
            Generate a list of visitors to check out and update the vis_cout_combobox.

            Args:
                event (Event, optional): The event that triggered the update. Defaults to None.

            Returns:
                list: A list of visitors to check out and their check-in times.
            """
            today = datetime.today().strftime("%m/%d/%y")
            visitors_list_today = []
            checkin_visit_time = []
            with open(visitation_path, 'r+') as file:
                file_data = json.load(file)
            for visit in file_data['visitation']:
                if visit["checkin_date"] == today and visit['checkout_time'] == "":
                    visitors_list_today.append(visit["vis_fullname"].title())
                    checkin_visit_time.append(visit['checkin_time'])
            if len(visitors_list_today) == 0:
                vis_cout_combobox.set("No Visitor")
                vis_cout_combobox.configure(state="disabled")
            if len(visitors_list_today) > 0:
                vis_cout_combobox.configure(state="readonly", values=visitors_list_today,
                                            command=checkout_visitor_entries)
                vis_cout_combobox.set(visitors_list_today[0])

            return [visitors_list_today, checkin_visit_time]

        def checkout_visitor(event=None):
            """
            Check out a visitor and record their checkout time and send a checkout message to the visitor's contact number.

            Args:
                event (Event, optional): The event that triggered the checkout. Defaults to None.
            """
            today = datetime.today().strftime("%m/%d/%y")
            current_time = datetime.now().strftime("%H:%M")
            visitor_to_checkout = vis_cout_fname.get() + " " + vis_cout_lname.get()

            with open(visitation_path, 'r+') as file:
                file_data = json.load(file)
                for visit in file_data['visitation']:
                    if visit["checkin_date"] == today:
                        if visit["vis_fullname"].lower() == visitor_to_checkout.lower() and visit[
                            "checkout_time"] == "":
                            visit['checkout_time'] = current_time
                            checkin_date = visit["checkin_date"]
                            checkin_date = datetime.strptime(checkin_date, "%m/%d/%y")
                            checkin_date = checkin_date.strftime("%b %d, %Y")
                            checkins_time = visit["checkin_time"]
                            checkout_time = visit['checkout_time']
                            resident = str(visit["res_fullname"]).title()
                            visitor = str(visit["vis_fullname"]).split()[0].title()
                            room = str(visit["res_room"]).title()
                            phone_number = visit["vis_cont"]

                            msg = CTkMessagebox(title="Success", message="Visitor successfully checked-out",
                                                icon="check",
                                                option_1="OK")
                            checkout_msg = f"Hello {visitor},\n\nWe hope you enjoyed visiting {resident} ({room}) on {checkin_date}, from {checkins_time} to {checkout_time}.\n\nSincerely,\nHeadington Hall Front Desk "
                            client = Client(secrets.account_sid, secrets.auth_token)
                            message = client.messages.create(
                                body=checkout_msg,
                                from_=secrets.twilio_number,
                                to=phone_number)
                            break

            with open(visitation_path, 'w') as file:
                json.dump(file_data, file, indent=1)

            vis_cout_fname.configure(state='normal')
            vis_cout_lname.configure(state='normal')
            vis_cout_fname.delete(0, tkinter.END)
            vis_cout_lname.delete(0, tkinter.END)
            change_cout_state()
            checkout_visitors_list()

        def cancel(event):
            """
            Cancel the checkout process and reset the checkout visitor entry fields.

            Args:
                event (Event): The event that triggered the cancellation.
            """
            vis_cout_fname.configure(state='normal')
            vis_cout_lname.configure(state='normal')
            vis_cout_fname.delete(0, tkinter.END)
            vis_cout_lname.delete(0, tkinter.END)
            change_cout_state()

        checkout_button.bind("<Button-1>", checkout_visitor)
        checkout_visitors_list()
        cancel_button = ctk.CTkButton(self, text="Cancel", width=95)
        cancel_button.place(relx=0.03, rely=0.94)
        cancel_button.bind("<Button-1>", cancel)

        # Activate the WeatherAPI to make this work
        # # Can readjust the location
        # weather_frame = WeatherDisplayFrame(self, height=180, width=180, corner_radius=150, border_width=8, border_color='#03396c')
        # weather_frame.place(relx=0.5, rely=0.1, anchor="n")


if __name__ == '__main__':
    app = App()
    app.mainloop()
