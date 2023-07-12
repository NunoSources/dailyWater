from plyer import notification
from datetime import datetime, date
from time import sleep
import sys
import os

log = "log.txt"
daily_water = "daily_water.txt"
last_record = "last_record.txt"
today = date.today().strftime("%d/%m/%Y")
daily_amounts = []
update = False
valid_answers = ["Y", "N", "YES", "NO"]
minutes = []

def format_current_minutes(minutes):
    if len(minutes) == 1:
        print(f"Current notification minute: ", end = "")
    elif len(minutes) > 1:
        print(f"Current notification minutes: ", end = "")
    print(*minutes, sep=", ")
    print()

def enter_minutes():
    while True:
        try:
            enter_minute = int(input("Enter one minute at a time to be notified at (-1 to confirm): "))
            if enter_minute == -1:
                if len(minutes) == 0:
                    print("You have to enter at least one minute.\n")
                else:
                    break
            elif not (-2 < enter_minute < 60):
                print("Enter a minute between 0 and 59.")
                format_current_minutes(minutes)
            else:
                if enter_minute in minutes:
                    print(f"You have already entered the minute {enter_minute}.")
                    format_current_minutes(minutes)
                else:
                    minutes.append(enter_minute)
                    print(f"Minute {enter_minute} successfully added.")
                    format_current_minutes(minutes)
        except ValueError:
            print("Only valid numbers are accepted.")
            format_current_minutes(minutes)
        except KeyboardInterrupt:
            print()
            print("~-" * 23, end = "~\n")
            print("You have stopped the program")
            print(f"The current amount of daily water is {amount} liters")
            print("~-" * 23, end = "~\n")
            sleep(1)
            print("Exiting the system... See you later!")
            print("~-" * 18, end = "~\n")
            sleep(1)
            sys.exit()
    return sorted(minutes)

def separator():
    print("~-" * 35, end = "~\n")

def read_from(filename):
    """ read from a file
    if the file is daily_water.txt or last_record.txt, it will return the current amount of water or last record
    if not, it will return the lines from log.txt as a list """
    try:
        with open(filename) as file:
            if filename == "daily_water.txt" or filename == "last_record.txt":
                return file.readline()
            return file.readlines()
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist or it's in a different location.")
        sys.exit()

def read_log():
    with open(log) as file:
        print(file.read())
       
def menu():
    print("~-" * 13, end = "~\n|")
    print("MENU".center(24),    "|")
    print("|", "/"*23, "|")
    print("| 1 - Open daily logs     |")
    print("| 2 - Update daily water  |")
    print("| 3 - Start the count     |")
    print("| 0 - Exit                |")
    print("~-" * 13, end = "~\n\n")

#reads the daily log
lines = read_from(log)     
if len(lines) == 0:
    with open(log, "w") as file:
        file.write(f"Water consumed {datetime.now().strftime('%A')} {today}:\n")
lines = read_from(log) 
#reads current amount of water from daily_water      
amount = read_from(daily_water)  
last_time_recorded = read_from(last_record)

if len(amount) == 0:
    with open(daily_water, "w") as file:
        file.write("0.0")
    amount = read_from(daily_water)

with open(log, "a") as file:
    if f"Water consumed {datetime.now().strftime('%A')} {today}:\n" not in lines:
        if "liters" not in lines[-2]: #if not yet, update to daily log, the amount of water consumed yesterday
            print("~-" * 18, end = "~\n")
            print("Updating yesterday's daily record...")
            print("~-" * 18, end = "~\n")
            sleep(1)
            file.write(f"{amount} liters\n\n")
            #lines = read_from(log) #update lines
            with open(daily_water, "w") as daily_file:
                daily_file.write("0.0")
            amount = read_from(daily_water)
        file.write(f"Water consumed {datetime.now().strftime('%A')} {today}:\n")
        lines = read_from(log) #update lines 

menu()

while True:
    sleep(1)
    option = input("Choose an option: ")
    print()
    if option == "1":
        os.system("cls")
        sleep(0.5)
        separator()
        print("YOUR DAILY LOG".center(70))
        separator()
        read_log()
        print("~-" * int(len(lines[0]) / 2), end = "~\n\n")
    elif option == "2":
        sleep(0.5)
        separator()
        print("UPDATE DAILY WATER".center(70))
        separator()
        print(f"Your current amount of water recorded on daily water is {amount} liters.")
        if len(last_time_recorded) == 0:
            print("There is no last record.")
        else:
            print(f"Last record at {last_time_recorded}")
        sleep(1)
        while True:
            try:
                new_amount = float(input("Enter the amount of water you drank after the last record: "))
                if new_amount == 0:
                    sleep(0.5)
                    print("Since you didn't drink any water after the last record, no daily water update is needed.\n")
                    break
                assert new_amount >= 0
            except AssertionError:
                print("You can't drink negative amount of water.")
            else:
                print("Updating daily water...")
                sleep(1)
                print("Daily water updated.\n")
                water = new_amount + float(amount)
                update = True
                with open(daily_water, "w") as file:
                    file.write(str(water))
                if new_amount > 0:
                    with open(last_record, "w") as file:
                        file.write(str(datetime.now().strftime("%H:%M:%S")))
                amount = read_from(daily_water)
                break
    elif option == "3":
        sleep(0.5)
        separator()
        print("START THE COUNT".center(70))
        separator()
        default_minutes = minutes = enter_minutes()
        print("\nYou'll be notified at the following minutes: ", end = "")
        print(*minutes, sep=", ")
        break
    elif option == "0":
        print("Exiting the system... See you later!")
        print("~-" * 18, end = "~\n")
        sleep(1)
        sys.exit()
    sleep(1)
    menu()
    
sleep(1)
separator()
print(f"Your current amount of water recorded on daily water is {amount} liters.")
if len(last_time_recorded) == 0:
    print("There is no last record.")
else:
    print(f"Last record at {last_time_recorded}")
separator()

sleep(1)
non_recorded_water = input("Did you drink any water after the last record? [Y/N]: ").upper() or "Y"
while non_recorded_water not in valid_answers:
    non_recorded_water = input("Enter a valid answer [Y/N]: ").upper() or "Y"
if non_recorded_water[0] == "Y":
    while True:
        try:
            new_amount = float(input("Enter the amount: "))
            if new_amount == 0:
                sleep(0.5)
                print("Since you didn't drink any water after the last record, no daily water update is needed.\n")
                break
            assert new_amount >= 0
        except AssertionError:
            print("You can't drink negative amount of water.")
        else:
            print("Updating daily water...")
            sleep(1)
            print("Daily water updated.")
            water = new_amount + float(amount)
            update = True
            with open(daily_water, "w") as file:
                file.write(str(water))
            if new_amount > 0:
                with open(last_record, "w") as file:
                    file.write(str(datetime.now().strftime("%H:%M:%S")))
            amount = read_from(daily_water)
            break
elif len(amount) != 0:
    water = float(amount)
sleep(0.5)
print("Running...")

def win_notification(water, update):
    if update == True:
        with open(daily_water, "w") as file: #writes on daily_water the amount of water at the moment
            file.write(str(water))
    else:
        amount = float(read_from(daily_water))
        with open(daily_water, "w") as file:
            file.write(str(amount + 0.250))
        water = amount + 0.250
    amount = read_from(daily_water)
    notification.notify(
        "Drink Water!",
        f"You drank {water} liters of water.",
        timeout = 10,
    )
    with open(last_record, "w") as file:
        file.write(str(datetime.now().strftime("%H:%M:%S")))
    return amount

while True:
    try:
        minutes = default_minutes     #chosen minutes for notifications
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        if current_minute in minutes:
            water += 0.250
            amount = win_notification(water, update)
            print(f"You drank {amount} liters of water by {read_from(last_record)}")
            print("Running...")
        sleep(60)
    except KeyboardInterrupt:
        separator()
        print("You have stopped the program")
        print(f"The current amount of daily water is {amount} liters")
        separator()
        if amount != '':
            sleep(1)
            update_log = input("Do you want to update daily log? [Y/N]: ").upper() or "Y"
            while update_log not in valid_answers:
                update_log = input("Enter a valid answer [Y/N]: ").upper() or "Y"
            if update_log[0] == "Y":
                print("Updating your daily log...")
                sleep(1)
                lines = read_from(log) #update lines 
                if f"Water consumed {datetime.now().strftime('%A')} {today}:\n" == lines[-1]:
                    with open(log, "a") as file:
                        file.write(f"{amount} liters\n\n")     #adds on log the amount of water from yesterday
                    print("Daily log updated successfully.")
                    with open(daily_water, "w") as file:
                        pass
                    water = float(0)
                    with open(daily_water, "w") as file:
                        file.write(str(water))
                else:
                    print("Daily log is already up to date.")
        sleep(1)
        print("Exiting the system... See you later!")
        print("~-" * 18, end = "~\n")
        sleep(1)
        sys.exit()
    