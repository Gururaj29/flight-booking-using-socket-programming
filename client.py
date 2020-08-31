import socket
import time
import pandas
#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting to server
s.connect(('127.0.0.1', 8908))

def authorization(signin):
	if signin=="y":
		print("Login with your details:")
		s.send("login".encode())
		print(50*"-")
		for i in range(3):
			email_id=input("Enter your email address\n")
			print(50*"-")
			s.send(email_id.encode())
			status=s.recv(10)
			password=input("Enter your password\n")
			print(50*"-")
			s.send(password.encode())
			status=s.recv(10).decode()
			if status != "1":
				if i!=2:
					print("Incorrect email or password. You can have %s more attempts."%(3-i-1))
					print(50*"-")
				else:
					print("Incorrect three attempts.")
					print(50*"-")
					s.close()
					return 0
			else:
				print("Logged in successfully")
				return 1
		#s.send()
	else:
		s.send("signup".encode())
		print("Fill the following details to signup\n")
		print(50*"-")
		first_name=input("Enter your first name\n")
		print(50*"-")
		last_name=input("Enter your last name\n")
		print(50*"-")
		email_id=input("Enter your email id\n")
		print(50*"-")
		password=input("Enter your password\n")
		print(50*"-")
		phone_number=input("Enter your phone number\n")
		print(50*"-")
		dob=input("Enter your data of birth in the form of dd/mm/yyyy\n")
		s.send(first_name.encode())
		status=s.recv(10)
		s.send(last_name.encode())
		status=s.recv(10)
		s.send(email_id.encode())
		status=s.recv(10)
		s.send(password.encode())
		status=s.recv(10)
		s.send(phone_number.encode())
		status=s.recv(10)
		s.send(dob.encode())
		print(s.recv(100).decode())
		print(50*'-')
		return 0

def menu():
	print("\nEnter any of the following keywords:\n")
	#print("menu: To check the list of keywords for various commands")
	print("(1) Check flights: To check all the flights for next two months")
	print("(2) View flight: To view details of a single flight")
	print("(3) Book tickets: To book seats in a flight for a single trip")
	print("(4) Order history: To look at all the flights booked earlier by this account")
	print("(5) Cancel tickets: To cancel seats of a flight")
	#print("round_trip: To book round trips of a flight")
	print("(6) Exit: To close the application")
	print(50*"-")

while True:
	signin=input("Do you have an account already?(y/n)\n")
	if authorization(signin):
		break
menu()
while True:
	print("AirIndia->",end=" ")
	cmd=input()
	if cmd!='menu':
		cmd=int(cmd)
		if cmd==1:
			cmd="check_flights"
		elif cmd==2:
			cmd="view_flight"
		elif cmd==3:
			cmd="book_tickets"
		elif cmd==4:
			cmd="order_history"
		elif cmd==5:
			cmd="cancel_tickets"
		elif cmd==6:
			cmd="exit"
	s.send(cmd.encode())
	if cmd=="menu":
		menu()
		status=s.recv(10)
	elif cmd=="check_flights":
		print(pandas.DataFrame.from_csv('data/flights_details.csv'))
		status=s.recv(10)
	elif cmd=="view_flight":
		status=s.recv(10)
		print("AirIndia/view_flight->",end=" ")
		flight_number=input("Enter a flight number\nAirIndia/view_flight->")
		df=pandas.DataFrame.from_csv('data/flights_details.csv')
		df=df[df.apply(lambda x:x["flight_number"]==flight_number,axis=1)]
		if df.empty:
			print("\nAirIndia/view_flight-> Invalid Flight number")
		else:
			print()
			for i in df.iterrows():
				print(i[1])
			df=pandas.DataFrame.from_csv('data/flights/%s.csv'%flight_number)

			for i in range(1,53):
				print("%s %s\t"%('A' if df["booking_status"][i-1]=="not_booked" else "B",i),end="")
				if i%4==0:
					print()
			print("A: Available seats\nB: Booked seats")
	elif cmd=="book_tickets":
		print("AirIndia/book_tickets->",end="")
		flight_number=input("Enter a flight number\nAirIndia/book_tickets->")
		df=pandas.DataFrame.from_csv('data/flights_details.csv')
		df=df[df.apply(lambda x:x["flight_number"]==flight_number,axis=1)]
		if df.empty:
			print("\nAirIndia/book_tickets-> Invalid Flight number")
		else:
			df=pandas.DataFrame.from_csv('data/flights/%s.csv'%flight_number)

			for i in range(1,53):
				print("%s %s\t"%('A' if df["booking_status"][i-1]=="not_booked" else "B",i),end="")
				if i%4==0:
					print()
			print("A: Available seats\nB: Booked seats")

			print("AirIndia/book_tickets->",end="")
			number_of_seats=int(input("Enter the number of seats to be booked\nAirIndia/book_tickets->"))
			msg="%s %s"%(flight_number,number_of_seats)
			s.send(msg.encode())
			
			for t in range(number_of_seats):
				print("AirIndia/book_tickets->",end="")
				
				seat_number=int(input("Enter a seat number\nAirIndia/book_tickets->"))
				if seat_number not in list(range(1,53)):
					print("\nInvalid seat number")
				else:
					msg="%s"%(seat_number)
					s.send(msg.encode())
					status=s.recv(50).decode()
					if status == "1":
						print("\nBooking successful")
					else:
						print("\nBooking Failed. Seat was already reserved or you are booking more than once for the same flight!")
					
	elif cmd == "order_history":
		user_id=s.recv(50).decode()
		df=pandas.DataFrame.from_csv("data/user_bookings/%s.csv"%user_id)
		if df.empty:
			print("\nNo seats booked yet")
		else:
			print(df)
	elif cmd == "cancel_tickets":
		print("AirIndia/cancel_tickets->",end="")
		flight_number=input("Enter a flight number\nAirIndia/book_tickets->")
		df=pandas.DataFrame.from_csv('data/flights_details.csv')
		df=df[df.apply(lambda x:x["flight_number"]==flight_number,axis=1)]
		if df.empty:
			print("\nAirIndia/cancel_tickets-> Invalid Flight number")
		else:
			print("AirIndia/cancel_tickets->",end="")
			number_of_seats=int(input("Enter the number of seats to be cancelled\nAirIndia/cancel_tickets->"))
			msg="%s %s"%(flight_number,number_of_seats)
			s.send(msg.encode())
			for i in range(number_of_seats):
				print("AirIndia/cancel_tickets->",end="")
				seat_number=int(input("Enter the seat number to be cancelled\nAirIndia/cancel_tickets->"))
				s.send(str(seat_number).encode())
				status=s.recv(50).decode()
				if status == "1":
					print("\nSeat successfully cancelled")
				else:
					print("\nSeat to be cancelled is not booked by you!")
	elif cmd=="exit":
		print("\nSession ended successfully")
		break
	else:
		print("\nEnter a valid command")
	print(50*"-")
s.close()

