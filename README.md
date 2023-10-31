# Headington Hall Visitation Logging System

## Overview

The Headington Hall Visitation Logging System is a project I initiated in early September with the aim of enhancing visitor management at Headington Hall, a prestigious residential facility at the University of Oklahoma. This system incorporates a wide range of features designed to facilitate visitor check-in, automate notifications, and minimize complications associated with the visitation log.

## Goal
The objective of this project was to streamline the tasks of a front desk clerk. Previously, manually inputting visitor information, such as first name, last name, check-in and check-out times, and the resident they were visiting, into a disorganized Excel sheet proved to be a cumbersome and time-consuming process. Recognizing the need for a more efficient system, I aimed to simplify the visitor check-in process by creating a link between visitor data and the corresponding resident, primarily through the resident's room number, a crucial piece of information.

My solution involved implementing a database to store visitor information and enable easy check-in and check-out procedures. This approach significantly reduced the time required for each visit's check-in and check-out process, making it more efficient.

## Key Features

- **User-Friendly Interface:** The system was developed using customtkinter, a framework that leverages the tkinter library module to create an aesthetically pleasing graphical user interface (GUI).

- **Real-Time Data Validation:** Data entered into the system is validated in real-time, reducing errors and ensuring accurate records.

- **Automated Notifications:** With the help of Twilio, the system automatically sends notifications containing the visitor's visit details upon their checkout.

## Limitation & Future Improvement 

The project utilized JSON files for data storage, offering a reliable NoSQL structure. However, this restricts its use to my personal access. To address this, my future goal is to transition to a NoSQL cloud database like MongoDB, enabling data storage and retrieval over the web.

Another limitation arises from the project's Python and customtkinter-based design, making it exclusive to Windows devices. To overcome this, I plan to transform the application into a web-based platform with enhanced access control for improved security. This transformation may present challenges, as it requires the utilization of new programming tools I haven't worked with before, such as Pyscript, ReactJS, Flask, and/or Firebase.

## App Layout
Images of the app layout can be located in the "GUI" folder, and a few examples are provided below.

<img src="https://github.com/EBOD13/visitation_log/blob/main/GUI/Screenshot%20(28).png" width="450" height="650" />


## Installation

To install and set up the Headington Hall Visitation Logging System, follow these steps:

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/EBOD13/your-repo.git
