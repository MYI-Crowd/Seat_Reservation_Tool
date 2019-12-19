from tkinter import *
from tkinter import messagebox

import csv


#Loads Floorplan for each floor from corresponding file
def loadReservations(filename):
	seats = []
	with open(filename, "r") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			seats.append(row)
	return seats

#Opens a new window and shows Floorplans for Foor 1 and Floor 2 as well as their status (booked / not booked)
def displayBookings():
	displayBookingsWdw = Toplevel()
	displayBookingsWdw.title("Floor Plans")
	displayBookingsWdw.configure(background = "blanched almond")
	displayBookingsWdw.columnconfigure(0, weight=1)
	displayBookingsWdw.rowconfigure(0, weight=0)
	displayBookingsWdw.iconbitmap("Seat.ico")

	Label(displayBookingsWdw, text="Seating Plan for Floor 1", font=("Helvetica", 12, "bold"), bg="blanched almond").grid(row=0, column=0, pady=10)

	i = 0

	for row in seats1:
		row_text = ' '.join(row)
		Label(displayBookingsWdw, text=row_text, bg="blanched almond").grid(row=i+1, column=0)
		i += 1

	Label(displayBookingsWdw, text="Seating Plan for Floor 2", font=("Helvetica", 12, "bold"), bg="blanched almond").grid(row=i+1, column=0, pady=10)
	i += 1
	for row in seats2:
		row_text = ' '.join(row)
		Label(displayBookingsWdw, text=row_text, bg="blanched almond").grid(row=i+1, column=0)
		i += 1

	Label(displayBookingsWdw, text="0 = Available, 1 = Occupied, 2 = Not a seat", bg = "blanched almond").grid(row=i+1, column=0, pady=10)

#This function opens a messagebox and asks the user if he wants to reserve the selected seat. If yes is pressed the seat is reserved. This function is called in the checkSeat function.
def reserve(floor,row,column):
	answer = messagebox.askyesno(title="Confirmation", message="Do you want to reserve this seat?")
	if answer == 1:
		floor[row][column] = '1'
		messagebox.showinfo(title="Success", message="Seat has been successfully reserved!")
	else:
		messagebox.showinfo(title="Cancelled", message="Your seat has not been reserved!")

#This function closes the main (root) window if the the user confirms.   
def quit():
	response = messagebox.askyesno(title="Warning", message="Are you sure you want to exit?")
	if response == 1:
		root.destroy()

#This function opens a new window and asks the user if he wants to check a seat in the first or second Floor. 
def checkSeat():
	checkSeatWdw = Toplevel()
	checkSeatWdw.title("Seat Reservation - Floor Selection")
	checkSeatWdw.configure(background = "blanched almond")
	checkSeatWdw.columnconfigure(0, weight=1)
	checkSeatWdw.rowconfigure(0, weight=0)
	checkSeatWdw.iconbitmap("Seat.ico")

	#This nested function gives the user the option to choose a floor and the corresponding row and column.
	def floor(floornr, seats):
		Label(checkSeatWdw, text="You selected Floor {}. Now select your row and column.".format(floornr), font=("Helvetica", 14), bg="blanched almond").grid(row=3, column=0, pady=20)
		Label(checkSeatWdw, text="Row", font=("Helvetica", 12), bg="blanched almond").grid(row=4, column=0, pady=10)
		Label(checkSeatWdw, text="Column", font=("Helvetica", 12), bg="blanched almond").grid(row=6, column=0, pady=10)

		clickedrow = IntVar()
		clickedcolumn = IntVar()
		length = len(seats)
		width = len(seats[0])
		length_list = [x for x in range(0, length)]
		width_list = [x for x in range(0, width)]
		RowSelect = OptionMenu(checkSeatWdw, clickedrow, *length_list).grid(row=5, column=0, pady=10)
		ColumnSelect = OptionMenu(checkSeatWdw, clickedcolumn, *width_list).grid(row=7, column=0, pady=10)
		return clickedrow, clickedcolumn

	#The confirm_floor function gives the user feedback about the status of his selected seat 
	def confirm_floor(seats, clickedrow, clickedcolumn):
		row = clickedrow.get()
		column = clickedcolumn.get()

		if seats[row][column]=='1':
			a = Label(checkSeatWdw, text="Sorry, this seat is already booked. Please select another one.", font=("Helvetica", 12), bg="blanched almond").grid(row=9, column=0, pady=10)
		elif seats[row][column]=='0':
			a = Label(checkSeatWdw, text="This seat is available.", font=("Helvetica", 12), bg="blanched almond").grid(row=9, column=0, pady=10)
			reserve(seats,row,column)    
		else:
			a = Label(checkSeatWdw, text="Sorry, this seat doesn't exist. Please select another one.", font=("Helvetica", 12), bg="blanched almond").grid(row=9, column=0, pady=10)

	#This function closes the window for selecting a seat. It is called in the "Close-Button" within the Floor1 & Floor2 function.
	def closewdw():
		checkSeatWdw.destroy()

	#This function executes the seat check for seats on the first floor after the "Confirm-Button" has been clicked after Floor1Btn ha been selected.
	def Floor1():
		clickedrow, clickedcolumn = floor(1, seats1)

		def confirm_floor1():
			confirm_floor(seats1, clickedrow, clickedcolumn)

		ConfirmBtn = Button(checkSeatWdw, width="15", text="Confirm", font=("Helvetica", 12), command=confirm_floor1).grid(row=8, column=0, pady=10)
		CloseBtn = Button(checkSeatWdw, width="15", text="Close", font=("Helvetica", 12), command=closewdw).grid(row=10, column=0, pady=10)

	#This function executes the seat check for seats on the first floor after the "Confirm-Button" has been clicked after Floor2Btn has been selected.
	def Floor2():

		clickedrow, clickedcolumn = floor(2, seats2)

		def confirm_floor2():
			confirm_floor(seats2, clickedrow, clickedcolumn)

		ConfirmBtn = Button(checkSeatWdw, width="15", text="Confirm", font=("Helvetica", 12), command=confirm_floor2).grid(row=8, column=0, pady=10)
		CloseBtn = Button(checkSeatWdw, width="15", text="Close", font=("Helvetica", 12), command=closewdw).grid(row=10, column=0, pady=10)

	Label(checkSeatWdw, text="On which floor do you want to reserve a seat?", font=("Helvetica", 14, "bold"), bg="blanched almond").grid(row=0, column=0, pady=50)

	Floor1Btn = Button(checkSeatWdw, width="25", text="Floor 1", font=("Helvetica", 12), command=Floor1).grid(row=1, column=0, pady=10)
	Floor2Btn = Button(checkSeatWdw, width="25", text="Floor 2", font=("Helvetica", 12), command=Floor2).grid(row=2, column=0, pady=10)

#This function reserves the first available seat on the selected floor, if there is a free seat available. It give the user information about the seat in a new window
def bookSeatonFloor(floornr, seats):
	bookSeatonFloorWdw = Toplevel()
	bookSeatonFloorWdw.title("Reserving an available seat on Floor {}".format(floornr))
	bookSeatonFloorWdw.configure(background = "blanched almond")
	bookSeatonFloorWdw.columnconfigure(0, weight=1)
	bookSeatonFloorWdw.rowconfigure(0, weight=0)
	bookSeatonFloorWdw.iconbitmap("Seat.ico")

	Label(bookSeatonFloorWdw, text="We have now reserved following seat for you on Floor {}: ".format(floornr), font=("Helvetica", 14, "bold"), bg="blanched almond").grid(row=0, column=0, pady=20)

	okBtn = Button(bookSeatonFloorWdw, text="OK", command=bookSeatonFloorWdw.destroy).grid(row=3, column=0, pady=10)
	#starts scanning the selected floor for empty seats and reserves the first seat that is available
	for row in range(0,len(seats)):
		for column in range(0,len(seats[row])):
			if seats[row][column]=='0':
				Label(bookSeatonFloorWdw, text="Row: " + str(row), bg="blanched almond").grid(row=1, column=0, pady=10)
				Label(bookSeatonFloorWdw, text="Column: " + str(column), bg="blanched almond").grid(row=2, column=0, pady=10)
				seats[row][column]='1'
				#Stop Searching
				return True
	#We scanned the whole floor without finding an empty seat:
	Label(bookSeatonFloorWdw, text="We couldn't find a seat on Floor {}. Please select another Floor.".format(floornr), bg="blanched almond").grid(row=1, column=0, pady=10)
	return False

#Calls the bookSeatonFloor function for floor 1 and the corresponding floor plan.
def bookSeatonFloor1():
	bookSeatonFloor(1, seats1)

#Calls the bookSeatonFloor function for floor 2 and the corresponding floor plan.
def bookSeatonFloor2():
	bookSeatonFloor(2, seats2)

#This function opens a new window and resets all reservations if the Admin Password has been entered correctly. It makes all existing seats available again.
def resetReservations():
	AdminWdw = Toplevel()
	AdminWdw.title("Admin")
	AdminWdw.configure(background = "blanched almond")
	AdminWdw.columnconfigure(0, weight=1)
	AdminWdw.rowconfigure(0, weight=0)
	AdminWdw.iconbitmap("Seat.ico")
	#This function checks for the Admin Password
	def checkpw():
		#Gets and checks Password from Entry-Widget
		PW = StringVar()
		PW = e.get()

		if PW == "1234":
			warnanswer = messagebox.askyesno(title="Warning", message="Are you sure you want to reset all reservations?")
			if warnanswer == 1:
				for row in range(0,len(seats1)):
					for column in range(0,len(seats1[row])):
						if seats1[row][column]=='1':
							seats1[row][column]='0'
				for row in range(0,len(seats2)):
					for column in range(0,len(seats2[row])):
						if seats2[row][column]=='1':
							seats2[row][column]='0'
				resetReservationsWdw = Toplevel()
				resetReservationsWdw.title("Cancellation")
				resetReservationsWdw.configure(background = "blanched almond")
				resetReservationsWdw.columnconfigure(0, weight=1)
				resetReservationsWdw.rowconfigure(0, weight=0)
				resetReservationsWdw.iconbitmap("Seat.ico")
				Label(resetReservationsWdw, text="All reservations have been reset.", bg="blanched almond").grid(row=0, column=0, pady=10)
				okRBtn = Button(resetReservationsWdw, text="OK", command=resetReservationsWdw.destroy).grid(row=1, column=0, pady=10)
			else:
				messagebox.showinfo(title="Cancelled", message="The reservations have not been reset.")
		else:
			lbl = Label(AdminWdw, text="Ha ha nice try intruder! Now back off!", bg="blanched almond").grid(row=3, column=0, pady=20)

	Label(AdminWdw, text="To perform the selected action, you need to sign in.", font=("Helvetica", 16, "bold"), bg="blanched almond").grid(row=0, column=0, pady=20)

	e = Entry(AdminWdw, width=20)
	e.grid(row=1, column=0, pady=20)
	e.insert(0, "Enter Admin Password")
	
	#This function shows a hint on the window if the Admin has forgotten his Password.
	def showhint():
		Label(AdminWdw, text="4321 but the other way around.", bg="blanched almond").grid(row=2, column=0)

	Button(AdminWdw, text="Confirm Password", command=checkpw).grid(row=4, column=0, pady=10)
	Button(AdminWdw, text="Oh I forgot. Can you give me a hint?", command=showhint).grid(row=5, column=0, pady=10)

	#This function opens a new window and counts how many seats are available on Floor 1 and Floor 2 and in total. 
def checkAvailability():
	checkAvailabilityWdw = Toplevel()
	checkAvailabilityWdw.title("Seat Availability")
	checkAvailabilityWdw.configure(background = "blanched almond")
	checkAvailabilityWdw.columnconfigure(0, weight=1)
	checkAvailabilityWdw.rowconfigure(0, weight=0)
	checkAvailabilityWdw.iconbitmap("Seat.ico")

	av1 = 0
	av2 = 0
	#counts available seats on floor 1 
	for row in seats1:
		for cell in row:
			if cell=='0':
				av1 += 1
    #counts available seats on floor 2
	for row in seats1:
		for cell in row:
			if cell=='0':
				av2 += 1
	#adds avilable seats on floor 1 and floor 2 together.
	avtot = av1 + av2
    
	Label(checkAvailabilityWdw, text="There are " + str(avtot) + " seats available.", bg="blanched almond").grid(row=0, column=0, pady=10)
	Label(checkAvailabilityWdw, text=str(av1) + " seats are available on Floor 1 and " + str(av2) + " seats are available on Floor 2", bg="blanched almond").grid(row=1, column=0, pady=10)

	okABtn = Button(checkAvailabilityWdw, text="OK", command=checkAvailabilityWdw.destroy).grid(row=2, column=0, pady=10)

#This function opens a new window and allows the user to cancel his reservation by selecting his seat. The window contains three dropdown menus: Floor, Row and Column for the user to select his seat.
def giveupseat():
	giveupseatWdw = Toplevel()
	giveupseatWdw.title("Give up Seat")
	giveupseatWdw.configure(background = "blanched almond")
	giveupseatWdw.columnconfigure(0, weight=1)
	giveupseatWdw.rowconfigure(0, weight=0)
	giveupseatWdw.iconbitmap("Seat.ico")
	#This function makes the selected seat available again.
	def cancel():

		floor = reservedfloor.get()
		row = reservedrow.get()
		column = reservedcolumn.get()

		if floor == 1:
			seats1[row][column]='0'
			Label(giveupseatWdw, text="You have successfully made the seat on Floor: %d , Row: %d , Column: %d available again." % (floor, row, column), bg="blanched almond").grid(row=7, column=0, pady=10)
		else:
			seats1[row][column]='0'
			Label(giveupseatWdw, text="You have successfully made the seat on Floor: %d , Row: %d , Column: %d available again." % (floor, row, column), bg="blanched almond").grid(row=7, column=0, pady=10)

	Label(giveupseatWdw, text="Floor", font=("Helvetica", 12), bg="blanched almond").grid(row=0, column=0, pady=10)
	Label(giveupseatWdw, text="Row", font=("Helvetica", 12), bg="blanched almond").grid(row=2, column=0, pady=10)
	Label(giveupseatWdw, text="Column", font=("Helvetica", 12), bg="blanched almond").grid(row=4, column=0, pady=10)

	reservedfloor = IntVar()
	reservedrow = IntVar()
	reservedcolumn = IntVar()

	max_length = max([len(seats1), len(seats2)])
	max_width = max([len(seats1[0]), len(seats2[0])])
	row_list = [x for x in range(0, max_length)]
	column_list = [x for x in range(0, max_width)]

	FloorGiveup = OptionMenu(giveupseatWdw, reservedfloor, 1, 2).grid(row=1, column=0, pady=10)
	RowGiveup = OptionMenu(giveupseatWdw, reservedrow, *row_list).grid(row=3, column=0, pady=10)
	ColumnGiveup = OptionMenu(giveupseatWdw, reservedcolumn, *column_list).grid(row=5, column=0, pady=10)

	ConfirmCancelBtn = Button(giveupseatWdw, text="Confirm", command=cancel).grid(row=6, column=0, pady=10)
    
	okSBtn = Button(giveupseatWdw, text="OK", command=giveupseatWdw.destroy).grid(row=8, column=0, pady=10)

#Main Program Starts Here
seats1 = loadReservations('seats1.csv')
seats2 = loadReservations('seats2.csv')

#Main Program Window. Initiates tkinter and opens the main window which presents the user with all possible functions.
root = Tk()
root.title("Learning Space Reservation Tool")
root.geometry("1000x1000")
root.configure(background = "blanched almond")
root.iconbitmap("Seat.ico")

Welcome = Label(root, text="Welcome to the learning space reservation tool!", font=("Helvetica", 20, "bold"), bg="blanched almond").grid(row=0, column=0, pady=20)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)

Selection = Label(root, text="What do you want to do?", font=("Helvetica", 16), bg="blanched almond").grid(row=1, column=0, pady=50)

ShowFloorplanBtn = Button(root, width=45, text="Show Floorplans", font=("Helvetica", 12), command=displayBookings).grid(row=2, column=0, pady=10)
OwnReservationBtn = Button(root, width=45, text="Reserve a seat of my choice", font=("Helvetica", 12), command=checkSeat).grid(row=3, column=0, pady=10)
ReservationFl1Btn = Button(root, width=45, text="Reserve a random seat on the first floor", font=("Helvetica", 12), command=bookSeatonFloor1).grid(row=4, column=0, pady=10)
ReservationFl2Btn = Button(root, width=45, text="Reserve a random seat on the second floor", font=("Helvetica", 12), command=bookSeatonFloor2).grid(row=5, column=0, pady=10)
CancelReservationBtn = Button(root, width=45, text="Cancel my reservation", font=("Helvetica", 12), command=giveupseat).grid(row=6, column=0, pady=10)
CheckAvailabilityBtn = Button(root, width=45, text="Check availability", font=("Helvetica", 12), command=checkAvailability).grid(row=7, column=0, pady=10)
ResetReservationBtn = Button(root, width=45, text="Reset all reservations", font=("Helvetica", 12), command=resetReservations).grid(row=8, column=0, pady=10)
ExitButton = Button(root, width=45, text="Exit program", font=("Helvetica", 12), fg="red", command=quit).grid(row=9, column=0, pady=10)

root.mainloop()
