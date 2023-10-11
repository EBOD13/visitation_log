import customtkinter as ctk
from PIL import Image
import requests
import sys
import tkinter
import json
from time import sleep, strftime
from datetime import datetime
import time
from itertools import cycle


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("400x650")
        self.iconbitmap('Headington Logo.ico')
        self.title("Headington Portal")
        self.resizable(False, False)
        self.ninja_API = "NINJA API KEY"

        city = 'norman'
        api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
        response = requests.get(api_url, headers={'X-Api-Key': self.ninja_API})

        current_time = datetime.now()
        # Calculate the time since the beginning of the day in milliseconds
        millisecond_since_startDay = (current_time - current_time.replace(hour=0, minute=0, second=0,
                                                                          microsecond=0)).total_seconds() * 1000

        if response.status_code == requests.codes.ok:
            sunset = response.json()['sunset']
        else:
            print("Error:", response.status_code, response.json)

        # Change the mode from daylight to nightlight

        if millisecond_since_startDay < sunset:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        self.login_screen = LoginScreen(self, self.winfo_screenheight(), self.winfo_screenwidth())
        self.main_screen = MainScreen(self, self.winfo_screenheight(), self.winfo_screenwidth())

        self.current_screen = None  # Track the current active screen
        self.show_main_screen()  # Show the login screen initially

    def show_login_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.login_screen.pack(fill='both', expand=True)
        self.current_screen = self.login_screen

    def show_main_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen if there is one
        self.main_screen.pack(fill='both', expand=True)
        self.current_screen = self.main_screen


class LoginScreen(ctk.CTkFrame):
    def __init__(self, container, app_height, app_width):
        super().__init__(container, height=app_height, width=app_width)

        # ctk.set_appearance_mode("light")
        def update_welcome_label(event):
            if len(name.get()) > 0:
                welcome_label.configure(text="Welcome " + name.get().title().strip())
            else:
                welcome_label.configure(text="Welcome to Headington Hall")

        # WELCOME TEXT
        welcome_label = ctk.CTkLabel(self, text="Welcome to Residence Hall",
                                     font=("Times", 20, "bold", "italic"), text_color="#841617", wraplength=250)
        welcome_label.place(relx=0.5, rely=0.08, anchor="n")

        # RESIDENCE LOGO
        my_image = ctk.CTkImage(light_image=Image.open("Residence Logo.png"), size=(72, 72))
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

        forgot_password = ctk.CTkEntry(self, placeholder_text="Name",
                                       height=45, width=300)

        def validate(filename='accounts.json'):
            with open(filename, 'r+') as file:
                file_data = json.load(file)

            for account in file_data['accounts']:
                if account.get('name').lower().strip() == name.get().lower().strip():
                    container.show_other_screen()
                else:
                    pass

        login_button = ctk.CTkButton(self, text="Login", height=40, width=300,
                                     corner_radius=65, fg_color="#841617",
                                     hover_color="#841617",  # Change hover color here
                                     border_width=2, text_color="#ffffff", border_color="#ffffff",
                                     command=lambda: validate())

        login_button.place(relx=0.5, rely=0.68, anchor="center")

class MainScreen(ctk.CTkFrame):

    def __init__(self, container, app_height, app_width):
        super().__init__(container, height=app_height, width=app_width)
        new_entry_label = ctk.CTkLabel(self, text="New Entry", font=("Times", 18, "bold"))
        new_entry_label.place(relx=0.03, rely=0.03)

        res_combobox = ctk.CTkComboBox(self, width=200, values="", variable="", state='disabled')
        res_combobox.place(relx=0.03, rely=0.15)
        vis_combobox = ctk.CTkComboBox(self, values="", variable="", width=200, state="disabled")
        vis_combobox.place(relx=0.55, rely=0.15)

        # data_file = open("people_profile.json")
        # json_file = json.load(data_file)

        def caps(event):
            fname_input.set(fname_input.get().title())
            lname_input.set(lname_input.get().title())
            room_input.set(room_input.get().title())

            mail_input.set(mail_input.get().lower())

        def change_state():
            vis_fname_entry.configure(state="readonly")
            vis_lname_entry.configure(state="readonly")
            vis_email_entry.configure(state="readonly")
            checkin_time.configure(state="readonly")
            date_entry.configure(state="readonly")

            res_fname_entry.configure(state="readonly")
            res_lname_entry.configure(state="readonly")
            res_email_entry.configure(state="readonly")

        fname_input = tkinter.StringVar()
        lname_input = tkinter.StringVar()
        room_input = tkinter.StringVar()
        mail_input = tkinter.StringVar()
        res_fname_entry = ctk.CTkEntry(self, placeholder_text="First Name", font=("Times", 14),
                                       textvariable=fname_input,
                                       width=200)
        res_fname_entry.place(relx=0.03, rely=0.25)
        res_fname_entry.bind("<KeyRelease>", caps)

        res_lname_entry = ctk.CTkEntry(self, placeholder_text="Last Name", font=("Times", 14), width=200,
                                       textvariable=lname_input, )
        res_lname_entry.place(relx=0.03, rely=0.35)
        res_lname_entry.bind("<KeyRelease>", caps)

        res_email_entry = ctk.CTkEntry(self, font=("Times", 14), placeholder_text="Email", width=200,
                                       textvariable=mail_input)
        res_email_entry.place(relx=0.03, rely=0.45)
        res_email_entry.bind("<KeyRelease>", caps)

        res_room_entry = ctk.CTkEntry(self, font=("Times", 14), width=95, placeholder_text="Room",
                                      textvariable=room_input)
        res_room_entry.place(relx=0.03, rely=0.55)
        res_room_entry.bind("<KeyRelease>", caps)

        # Visitor's panel side

        vis_lname_entry = ctk.CTkEntry(self, font=("Times", 14), width=200)
        vis_email_entry = ctk.CTkEntry(self, font=("Times", 14), width=200)
        submit_button = ctk.CTkButton(self, text="Submit", font=("Times", 14), width=200)
        vis_fname_entry = ctk.CTkEntry(self, font=("Times", 14), width=200)
        checkin_time = ctk.CTkEntry(self, font=("Times", 14), width=50)
        date_entry = ctk.CTkEntry(self, font=("Times", 14), width=67)
        checkout_time = ctk.CTkEntry(self, font=("Times", 14), width=50)

        vis_fname_entry.place(relx=0.55, rely=0.25)
        vis_lname_entry.place(relx=0.55, rely=0.35)
        vis_email_entry.place(relx=0.55, rely=0.45)
        checkin_time.place(relx=0.725, rely=0.55)
        date_entry.place(relx=0.55, rely=0.55)
        checkout_time.place(relx=0.85, rely=0.55)
        submit_button.place(relx=0.55, rely=0.65)

        def fill_visitor_entries(choice):
            time_now = datetime.now().strftime("%H:%M")
            today = datetime.today().strftime("%m/%d/%y")
            vis_fname_entry.configure(state="normal")
            vis_lname_entry.configure(state="normal")
            vis_email_entry.configure(state="normal")
            checkin_time.configure(state="normal")
            date_entry.configure(state="normal")

            vis_fname_entry.delete(0, tkinter.END)
            vis_lname_entry.delete(0, tkinter.END)
            vis_email_entry.delete(0, tkinter.END)
            checkin_time.delete(0, tkinter.END)
            date_entry.delete(0, tkinter.END)

            checkin_time.insert(0, time_now)
            date_entry.insert(0, today)
            vis_fname_entry.insert(0, choice.split(" ")[0])
            vis_lname_entry.insert(0, choice.split(" ")[1])

            for i in range(len(make_visitor_list()[1])):
                if choice.split(" ")[0] == make_visitor_list()[1][i].split(" ")[0] and choice.split(" ")[1] == \
                        make_visitor_list()[1][i].split(" ")[1]:
                    vis_email_entry.configure(state="normal")
                    vis_email_entry.insert(0, make_visitor_list()[1][i].split(" ")[2])
            change_state()

            return choice.split(" ")[0] + " " + choice.split(" ")[1]

        def fill_resident_entries(choice):
            res_fname_entry.configure(state="normal")
            res_lname_entry.configure(state="normal")
            res_email_entry.configure(state="normal")

            res_fname_entry.delete(0, tkinter.END)
            res_lname_entry.delete(0, tkinter.END)
            res_email_entry.delete(0, tkinter.END)

            res_fname_entry.insert(0, choice.split(" ")[0])
            res_lname_entry.insert(0, choice.split(" ")[1])

            for i in range(len(make_resident_list()[1])):
                if choice.split(" ")[0] == make_resident_list()[1][i].split(" ")[0] and choice.split(" ")[1] == \
                        make_resident_list()[1][i].split(" ")[1]:
                    res_email_entry.configure(state="normal")
                    res_email_entry.delete(0, tkinter.END)
                    res_email_entry.insert(0, make_resident_list()[1][i].split(" ")[2])

            # Clear previously filled visitor entries
            vis_fname_entry.configure(state="normal")
            vis_lname_entry.configure(state="normal")
            vis_email_entry.configure(state="normal")
            checkin_time.configure(state="normal")
            vis_fname_entry.delete(0, tkinter.END)
            vis_lname_entry.delete(0, tkinter.END)
            vis_email_entry.delete(0, tkinter.END)
            checkin_time.delete(0, tkinter.END)

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

            change_state()

            return choice.split(" ")[0] + " " + choice.split(" ")[1]

        def make_resident_list(event=None, filename="people_profile.json"):
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
                # Handle the case when no residents are found
                res_fname_entry.configure(state="normal")
                res_lname_entry.configure(state="normal")
                res_email_entry.configure(state="normal")
                res_fname_entry.delete(0, tkinter.END)
                res_lname_entry.delete(0, tkinter.END)
                res_email_entry.delete(0, tkinter.END)
                res_combobox_var = ctk.StringVar(value="No Residents Found")

            res_combobox.configure(values=list_of_residents, variable=res_combobox_var, width=200,
                                   command=fill_resident_entries, state="readonly")

            # res_combobox.configure(state="readonly")

            # res_combobox.place(relx=0.03, rely=0.15)

            def update_visitor_list(event=None):
                # Only update the visitor list if both res_fname_entry and res_combobox have valid values
                if res_combobox.get() == "No Residents Found":
                    make_visitor_list()

            update_visitor_list()

            return [list_of_residents, list_of_resMails]

        def make_visitor_list(event=None, filename="people_profile.json"):
            res_fname = res_fname_entry.get()
            res_lname = res_lname_entry.get()
            # res_room = res_room_entry.get()
            full_name = f"{res_fname.lower()} {res_lname.lower()}"

            with open(filename, 'r+') as file:
                file_data = json.load(file)

            # Create a list to store visitor names
            list_of_visitors = []
            list_of_mails = []

            # Collect visitor names
            for resident in file_data['residents']:
                if resident['full_name'].lower() == full_name.lower():
                    for visitor in resident["visitors"]:
                        # Append visitor's full name to the list
                        list_of_visitors.append(visitor.get('vis_fullname').title())
                        list_of_mails.append(
                            visitor.get('vis_fullname').title() + " " + visitor.get('vis_email').lower())

            if len(list_of_visitors) > 0:
                vis_combobox_var = ctk.StringVar(value=list_of_visitors[0])
            else:
                vis_fname_entry.configure(state="normal")
                vis_lname_entry.configure(state="normal")
                vis_email_entry.configure(state="normal")
                checkin_time.configure(state="normal")
                date_entry.configure(state='normal')
                vis_fname_entry.delete(0, tkinter.END)
                vis_lname_entry.delete(0, tkinter.END)
                vis_email_entry.delete(0, tkinter.END)
                checkin_time.delete(0, tkinter.END)
                date_entry.delete(0, tkinter.END)

                vis_combobox_var = ctk.StringVar(value="No visitor found")

            vis_combobox.configure(state="readonly", variable=vis_combobox_var, values=list_of_visitors,
                                   command=fill_visitor_entries)
            return [list_of_visitors, list_of_mails]

        # Bind the make_visitor_list function to changes in the res_fname_entry
        res_fname_entry.bind("<KeyRelease>", make_visitor_list)
        entry_next_button = ctk.CTkButton(self, text="Enter", font=("Times", 14), width=95,
                                          command=make_visitor_list)
        entry_next_button.place(relx=0.24, rely=0.55)

        def add_resident(res_fname, res_lname, res_email, res_room, filename="people_profile.json"):
            full_name = res_fname.lower() + " " + res_lname.lower()
            resident_profile = {"full_name": full_name,
                                "email": res_email.lower(),
                                "room": res_room.lower(),
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

        def add_visitor(vis_fname, vis_lname, vis_email, res_room, res_name, filename="people_profile.json"):
            vis_full_name = f"{vis_fname.lower()} {vis_lname.lower()}"
            visitor_profile = {"vis_fullname": vis_full_name, "vis_email": vis_email}

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
                        existing_emails = {v['vis_email'] for v in resident['visitors']}
                        # Check if the new visitor's full name and email are not in the existing set
                        if vis_full_name.lower() not in existing_names or vis_email.lower() not in existing_emails:
                            resident['visitors'].append(visitor_profile)
                            file.seek(0)
                            json.dump(file_data, file, indent=1)

        def chekin_visitor(vis_fname, vis_lname, vis_email, res_room, res_name, checkin_time, checkout_time, checkin_date,
                           filename="visitation_log.json"):
            vis_full_name = f"{vis_fname.lower()} {vis_lname.lower()}"
            visitor_profile = {"checkin_date": checkin_date,
                               "res_fullname": res_name,
                               "vis_fullname": vis_full_name,
                               "res_room": res_room,
                               "vis_email": vis_email,
                               "checkin_time": checkin_time,
                               "checkout_time": checkout_time}

            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data['visitation'].append(visitor_profile)
                file.seek(0)
                json.dump(file_data, file, indent=1)


        # BINDING ENTER EVENT TO MAKING THE LIST OF ALL RESIDENTS
        res_room_entry.bind("<KeyRelease>", make_resident_list)


if __name__ == '__main__':
    app = App()
    app.mainloop()
