from tkinter import *
from tkinter import filedialog
import string
import os
import csv
import sys
import subprocess

os.chdir(sys._MEIPASS)

filters = []
alphabet_list = []
req_all = False
file_path = ""
confirm_send = False
send_to_everyone = False

def send_message():
    global send_to_everyone
    global confirm_send
    if not confirm_send:
        confirm.grid(row=5)
        everyone.grid(row=4)
        confirm_send = True
    else:
        confirm.grid_forget()
        everyone.deselect()
        everyone.grid_forget()
        confirm_send = False

        MESSAGE = message_input.get("1.0", 'end-1c')
        if MESSAGE and (len(filters) > 0 or send_to_everyone) and not MESSAGE.isspace():
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                contacted_numbers = []
                for row in reader:
                    if send_to_everyone or (req_all and all(row[filter[0]] == filter[1] for filter in filters)) or (not req_all and any(row[filter[0]] == filter[1] for filter in filters)):
                        number_index = alphabet_list.index(number_alphabet_dropdown_value.get())
                        RECIPIENT_NUMBER = row[number_index].replace('-', '')
                        if RECIPIENT_NUMBER.isnumeric() and all(int(RECIPIENT_NUMBER) != int(number) for number in contacted_numbers):
                            contacted_numbers.append(RECIPIENT_NUMBER)
                            subprocess.Popen(['osascript', 'sendmessage.txt', RECIPIENT_NUMBER, MESSAGE], stdout=subprocess.PIPE)
        send_to_everyone = False


def add_filter():
    filter = dropdown_text.get()
    if len(filters) < 5:
        filters.append([alphabet_list.index(alphabet_dropdown_value.get()), filter])
        filter_labels.append(Label(filter_frame, font=("Arial", 11)))
        filter_labels[len(filters) - 1].config(
            text="From column " + str(list(alphabet_list)[filters[len(filters) - 1][0]]) + " find \"" + str(
                filters[len(filters) - 1][1]) + "\"")
        filter_labels[len(filters) - 1].grid(row=len(filters))


def clear_filter():
    global filters, filter_labels
    filters = []
    for label in filter_labels:
        label.destroy()
    filter_labels = []


def change_req():
    global req_all
    req_all = not req_all

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if not file_path.endswith(".csv"):
        return

    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        column_size = len(list(reader)[0])

    letters = [''] + list(string.ascii_uppercase)
    for column in range(column_size):
        alphabet_list.append(letters[column // 26] + list(string.ascii_uppercase)[column % 26])

    message_frame.grid(row=0)
    filter_dropdown_frame.grid(row=1)

    alphabet_dropdown = OptionMenu(dropdown_frame, alphabet_dropdown_value, *alphabet_list)
    alphabet_dropdown.grid(row=1)

    dropdown_frame.grid(row=0, column=0, pady=10, padx=5)
    filter_frame.grid(row=0, column=1, pady=10, padx=5)

    number_alphabet_dropdown = OptionMenu(number_frame, number_alphabet_dropdown_value, *alphabet_list)
    number_alphabet_dropdown.grid(row=1)

    number_frame.grid(row=2, pady=10)
    submit.grid(row=3)

def change_everyone():
    global send_to_everyone
    send_to_everyone = not send_to_everyone
    print(send_to_everyone)

window = Tk()
window.title('HIM Automatic Message Sender')
window.resizable(False, False)
window.config()

file_input = Button(window, text="Upload .csv File", command=open_file)
file_input.grid(row=0)

message_frame = Frame(window, borderwidth=1, relief="groove")
filter_dropdown_frame = Frame(window, borderwidth=1, relief="groove")
dropdown_frame = Frame(filter_dropdown_frame, borderwidth=1, relief="groove")
filter_frame = Frame(filter_dropdown_frame, borderwidth=1, relief="groove")
number_frame = Frame(window, borderwidth=1, relief="groove")

message_label = Label(message_frame)
message_label.config(text="Message")
message_label.grid(row=0)

message_input = Text(message_frame)
message_input.config(width=50, height=15)
message_input.grid(row=1)

alphabet_dropdown_label = Label(dropdown_frame)
alphabet_dropdown_label.config(text="Google Sheets Column")
alphabet_dropdown_label.grid(row=0)

alphabet_dropdown_value = StringVar(window, "A")

dropdown_text_label = Label(dropdown_frame)
dropdown_text_label.config(text="Targeted Value")
dropdown_text_label.grid(row=2)

dropdown_text = Entry(dropdown_frame)
dropdown_text.grid(row=3)

filter = Button(dropdown_frame, text="Add Filter", command=add_filter)
filter.grid(row=4)

filter_labels = []

filter_text_label = Label(filter_frame)
filter_text_label.config(text="Filters Added (Max 5)")
filter_text_label.grid(row=0)

filter = Button(filter_frame, text="Clear Filters", command=clear_filter)
filter.grid(row=7)

cb = Checkbutton(filter_frame, text="Must meet all requirements.", command=change_req)
cb.grid(row=8)

number_alphabet_dropdown_label = Label(number_frame)
number_alphabet_dropdown_label.config(text="Phone Number Column")
number_alphabet_dropdown_label.grid(row=0)

number_alphabet_dropdown_value = StringVar(window, "A")

confirm = Label(window)
confirm.config(text="Click again to confirm.", fg="#ff0000")

submit = Button(window, text="Send", command=send_message)

everyone = Checkbutton(window, text="Send to everyone.", command=change_everyone)

window.mainloop()
