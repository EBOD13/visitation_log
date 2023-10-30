import customtkinter as ctk
from twilio.rest import Client
from PIL import Image
from CTkMessagebox import CTkMessagebox
import re
import tkinter
import json
from datetime import datetime
import secrets


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("500x700")
        self.iconbitmap(r"venv/data/images/Headington Logo.ico")
        self.title("Headington Portal")
        self.resizable(False, False)
        self.login_screen = LoginScreen(self, self.winfo_screenheight(), self.winfo_screenwidth())
        self.main_screen = MainScreen(self, self.winfo_screenheight(), self.winfo_screenwidth())
        self.other_screen = OtherScreen(self, self.winfo_screenheight(), self.winfo_screenwidth())
        self.current_screen = None  # Track the current active screen
        self.show_main_screen()  # Show the login screen initially

    def show_login_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.login_screen.pack(fill='both', expand=True)
        self.current_screen = self.login_screen

    def show_other_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.other_screen.pack(fill='both', expand=True)
        self.current_screen = self.other_screen

    def show_main_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.main_screen.pack(fill='both', expand=True)
        self.current_screen = self.main_screen


class LoginScreen(ctk.CTkFrame):
    def __init__(self, container, app_height, app_width):
        super().__init__(container, height=app_height, width=app_width)
        ctk.set_appearance_mode("light")

        def update_welcome_label(event=None):
            if len(name.get()) > 0:
                welcome_label.configure(text="Welcome " + name.get().title().strip())
            else:
                welcome_label.configure(text="Welcome to Headington Hall")

        # WELCOME TEXT
        welcome_label = ctk.CTkLabel(self, text="Welcome to Headington Hall",
                                     font=("Times", 20, "bold", "italic"), text_color="#841617", wraplength=250)
        welcome_label.place(relx=0.5, rely=0.08, anchor="n")

        # HEADINGTON LOGO
        logo = "venv/data/images/Headington Logo.png"
        accounts_path = r"venv/data/json_files/accounts.json"
        my_image = ctk.CTkImage(light_image=Image.open(logo), size=(72, 72))
        image_label = ctk.CTkLabel(self, image=my_image, text="")
        image_label.place(relx=0.5, rely=0.24, anchor="center")

        name = ctk.CTkEntry(self, placeholder_text="Name",
                            height=45, width=300)
        work_id = ctk.CTkEntry(self, placeholder_text="Work ID",
                               height=45, width=300)
        password = ctk.CTkEntry(self, placeholder_text="Password", height=45, width=300,
                                show="*")  # Show password as asterisks
        name.place(relx=0.5, rely=0.38, anchor="center")
        name.bind('<FocusOut>', update_welcome_label)
        work_id.place(relx=0.5, rely=0.48, anchor="center")
        password.place(relx=0.5, rely=0.58, anchor="center")

        # forgot_password = ctk.CTkEntry(self, placeholder_text="Name",
        #                                height=45, width=300)

        def validate(filename=accounts_path):
            with open(filename, 'r+') as file:
                file_data = json.load(file)

            for account in file_data['accounts']:
                if account.get('name').lower().strip() == name.get().lower().strip():
                    container.show_main_screen()
                else:
                    pass

        login_button = ctk.CTkButton(self, text="Login", height=40, width=300,
                                     corner_radius=65, fg_color="#841617",
                                     hover_color="#841617",  # Change hover color here
                                     border_width=2, text_color="#ffffff", border_color="#ffffff",
                                     command=lambda: validate())

        login_button.place(relx=0.5, rely=0.68, anchor="center")


class OtherScreen(ctk.CTkFrame):
    def __init__(self, container, app_height, app_width):
        super().__init__(container, height=app_height, width=app_width)

        # WELCOME TEXT
        welcome_label = ctk.CTkLabel(self, text="Screen 2",
                                     font=("Times", 20, "bold", "italic"), text_color="#841617", wraplength=250)
        welcome_label.place(relx=0.5, rely=0.15, anchor="n")

        # HEADINGTON LOGO
        # my_image = ctk.CTkImage(light_image=Image.open("Headington Logo.png"), size=(72, 72))
        # image_label = ctk.CTkLabel(self, image=my_image, text="")
        # image_label.place(relx=0.5, rely=0.25, anchor="center")

        name = ctk.CTkEntry(self, placeholder_text="Name",
                            height=45, width=300)
        work_id = ctk.CTkEntry(self, placeholder_text="Work ID",
                               height=45, width=300)
        password = ctk.CTkEntry(self, placeholder_text="Password", height=45, width=300,
                                show="*")  # Show password as asterisks
        login_button = ctk.CTkButton(self, text="Login", height=40, width=300,
                                     corner_radius=65, fg_color="#841617",
                                     hover_color="#841617",  # Change hover color here
                                     border_width=2, text_color="#ffffff", border_color="#ffffff",
                                     command=lambda: container.show_login_screen())
        name.place(relx=0.5, rely=0.40, anchor="center")
        work_id.place(relx=0.5, rely=0.50, anchor="center")
        password.place(relx=0.5, rely=0.60, anchor="center")
        login_button.place(relx=0.5, rely=0.70, anchor="center")


class MainScreen(ctk.CTkFrame):

    def __init__(self, container, app_height, app_width):
        super().__init__(container, height=app_height, width=app_width)
        new_entry_label = ctk.CTkLabel(self, text="New Entry", font=("Times", 18, "bold"))
        new_entry_label.place(relx=0.03, rely=0.03)
        res_combobox = ctk.CTkComboBox(self, width=200, values=None, variable=None, state='disabled')
        res_combobox.place(relx=0.03, rely=0.25)
        vis_combobox = ctk.CTkComboBox(self, values=None, variable=None, width=200, state="disabled")
        vis_combobox.place(relx=0.55, rely=0.25)
        checkout_button = ctk.CTkButton(self, text="Check Out", width=95, fg_color="#841617",
                                        hover_color='#991112')
        checkout_button.place(relx=0.24, rely=0.94)
        visitation_path = r"venv/data/json_files/visitation_log.json"
        people_path = r"venv/data/json_files/people_profile.json"

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
        validate_func = self.register(validate_input)

        def set_entry_limit(room):
            if len(room_input.get()) > 0:
                room_input.set(room_input.get()[:4])

        # Function to change the states of the widgets
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
        search_room_label = ctk.CTkLabel(self, text="Search by Room:", font=("Times", 15))  # Search by room label
        res_label = ctk.CTkLabel(self, text="Visitor Information",
                                 font=("Times", 20, "bold", "italic"), )  # Search by room label
        res_fname_label = ctk.CTkLabel(self, text="First Name:", font=("Times", 14))  # Search by room label
        res_lname_label = ctk.CTkLabel(self, text="Last Name:", font=("Times", 14))  # Search by room label
        res_mail_label = ctk.CTkLabel(self, text="Email:", font=("Times", 14))  # Search by room label
        vis_fname_label = ctk.CTkLabel(self, text="First Name:", font=("Times", 14))  # Search by room label
        vis_lname_label = ctk.CTkLabel(self, text="Last Name:", font=("Times", 14))  # Search by room label
        vis_cont_label = ctk.CTkLabel(self, text="Phone number:", font=("Times", 14))  # Search by room label

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
        res_room_entry = ctk.CTkEntry(self, font=("Times", 14), width=90, textvariable=room_input)  # Resident Room
        res_fname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=fname_input,
                                       width=200)  # Resident Firstname
        res_lname_entry = ctk.CTkEntry(self, font=("Times", 14), width=200,
                                       textvariable=lname_input)  # Resident Lastname
        res_email_entry = ctk.CTkEntry(self, font=("Times", 14), width=200, textvariable=mail_input)  # Resident Email
        # Visitors
        vis_fname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=vis_fname_input, width=200)
        vis_lname_entry = ctk.CTkEntry(self, font=("Times", 14), textvariable=vis_lname_input, width=200)
        vis_cont_entry = ctk.CTkEntry(self, validate="key", validatecommand=(validate_func, "%P"))
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
            res_room = str(re.findall("[A-Za-z]\\d{3}", res_room_entry.get())[0])
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
                    file_data['residents'].append(resident_profile)
                    file.seek(0)
                    json.dump(file_data, file, indent=1)
                # Else, if the resident is not empty, then check if the given data corresponds to any of the resident
                # information in the system. If there is no match, use the new data to create a new resident
                elif all(file_data.get('residents')) and not any(
                        resident.get('full_name', '').lower() == full_name.lower() for resident in
                        file_data.get('residents', [])):
                    file_data['residents'].append(resident_profile)
                    file.seek(0)
                    json.dump(file_data, file, indent=1)

        def fill_visitor_entries(choice):
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
            res_room = res_room_entry.get().strip()  # Ensure you have a valid res_room_entry
            with open(filename, 'r+') as file:
                file_data = json.load(file)

            # Create a list to store resident names
            list_of_residents = []
            list_of_resMails = []

            # Collect resident names
            for resident in file_data['residents']:
                if resident['room'].lower() == res_room.lower():
                    # Append resident's full name to the list
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

        # Function used to check in visitors
        def checkin_visitor(vis_fname, vis_lname, vis_cont, res_room, res_name, filename=visitation_path):
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

            else:  # Add the new visitor to the list
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
                                            # clear("all")

                                        # Update the vis_combobox with no visitors found
                                        except json.JSONDecodeError:
                                            msg = CTkMessagebox(title="Error", message="Error: Submission unsuccessful."
                                                                , icon="cancel",
                                                                option_1="OK")
                                        # clear("all")
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
            vis_cout_fname.configure(state="readonly")
            vis_cout_lname.configure(state="readonly")

        def checkout_visitor_entries(choice):
            # time_now = datetime.now().strftime("%H:%M")
            # today = datetime.today().strftime("%m/%d/%y")
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
                vis_cout_combobox.configure(state="readonly", values=visitors_list_today, command=checkout_visitor_entries)
                vis_cout_combobox.set(visitors_list_today[0])

            return [visitors_list_today, checkin_visit_time]

        def send_checkout_msg(phone_number):
            with open(visitation_path, 'r+') as file:
                file_data = json.load(file)
                today = datetime.today().strftime("%m/%d/%y")
                for visit in file_data['visitation']:
                    if visit["vis_fullname"].lower() != "" and visit["checkin_time"] != "" and visit["checkout_time"] != "" and \
                            visit["checkin_date"] == today:
                        checkin_date = visit["checkin_date"]
                        checkin_date = datetime.strptime(checkin_date, "%m/%d/%y")
                        checkin_date = checkin_date.strftime("%b %d, %Y")
                        checkin_time = visit["checkin_time"]
                        checkout_time = visit['checkout_time']
                        resident = str(visit["res_fullname"]).title()
                        visitor = str(visit["vis_fullname"]).split()[0].title()
                        room = str(visit["res_room"]).title()
                        vis_cont_num = visit["vis_cont"]

                        checkout_msg = f"Hello {visitor},\n\nWe hope you enjoyed visiting {resident} ({room}) on {checkin_date}, from {checkin_time} to {checkout_time}.\n\nSincerely,\nHeadington Hall Front Desk "
                        try:
                            client = Client(secrets.account_sid, secrets.auth_token)
                            message = client.messages.create(
                                body=checkout_msg,
                                from_=secrets.twilio_number,
                                to=phone_number)
                        except Exception as e:
                            print(e)

        def checkout_visitor(event=None):
            today = datetime.today().strftime("%m/%d/%y")
            current_time = datetime.now().strftime("%H:%M")
            visitor_to_checkout = vis_cout_fname.get() + " " + vis_cout_lname.get()

            with open(visitation_path, 'r+') as file:
                file_data = json.load(file)
                for visit in file_data['visitation']:
                    if visit["checkin_date"] == today:
                        if visit["vis_fullname"].lower() == visitor_to_checkout.lower() and visit["checkout_time"] == "":
                            visit['checkout_time'] = current_time
                            msg = CTkMessagebox(title="Success", message="Visitor successfully checked-out", icon="check",
                                                option_1="OK")
                            send_checkout_msg(visit["vis_cont"])  # Send the message after updating checkout time
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




if __name__ == '__main__':
    app = App()
    app.mainloop()
