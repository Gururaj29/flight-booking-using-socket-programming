import socket
import pandas
# creating a socket to listen for incoming connections
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding hostname and port number to socket
# serversocket.bind((socket.gethostname(), 8888))
serversocket.bind(('',8908))
# dont bind on the localhost
# listening for connections
SIGN_UP="signup"
LOGIN="login"
EXIT="exit"
BOOK_TICKETS="book_tickets"
CHECK_FLIGHTS="check_flights"
VIEW_FLIGHT="view_flight"
ORDER_HISTORY="order_history"
CANCEL_TICKETS="cancel_tickets"
MENU="menu"
flag=0
serversocket.listen(1)
while True:
	# accepting connection from client
	clientsocket, addr = serversocket.accept()
	print("Connected to client")
	while True:
		message=clientsocket.recv(1000)
		message=message.decode()
		if message == EXIT:
			break
		elif message == SIGN_UP:
			user_df=pandas.DataFrame.from_csv("data/user_data.csv")
			df={"first_name":[],"last_name":[],"email_id":[],"password":[],"phone_number":[],"dob":[],"user_id":[]}
			first_name=clientsocket.recv(1000)
			clientsocket.send("1".encode())
			last_name=clientsocket.recv(1000)
			clientsocket.send("1".encode())	
			email_id=clientsocket.recv(1000)
			clientsocket.send("1".encode())
			password=clientsocket.recv(1000)
			clientsocket.send("1".encode())
			phone_number=clientsocket.recv(1000)
			clientsocket.send("1".encode())
			dob=clientsocket.recv(1000)
			df["first_name"].append(first_name.decode())
			df["last_name"].append(last_name.decode())
			df["email_id"].append(email_id.decode())
			df["password"].append(password.decode())
			df["phone_number"].append(phone_number.decode())
			df["dob"].append(dob.decode())
			user_id=11000 if user_df.empty else 11000+len(user_df.email_id.dropna())
			df["user_id"]=user_id
			df=pandas.DataFrame(df)
			if user_df.empty==True or user_df[user_df.apply(lambda x: x['email_id']==email_id.decode(),axis=1)].empty==True:

				user_df=user_df.append(df)
				user_df.to_csv("data/user_data.csv")
				clientsocket.send("Registered successfully".encode())
				pandas.DataFrame({"depart_code":[],"dest_code":[],"flight_number":[],"journey_time":[],"number_of_seats":[]}).to_csv("data/user_bookings/%s.csv"%user_id)
			else:
				clientsocket.send("Email address already exists. Registeration unsuccessful.".encode())
		elif message==LOGIN:
			user_df=pandas.DataFrame.from_csv('data/user_data.csv')
			for i in range(3):
				email_id=clientsocket.recv(50)
				clientsocket.send("1".encode())
				password=clientsocket.recv(50)
				if user_df[user_df.apply(lambda x: x['email_id']==email_id.decode() and x['password']==password.decode(),axis=1)].empty==True:
					clientsocket.send("0".encode())
					if i==2:
						clientsocket.close()
						flag=1
				else:
					clientsocket.send("1".encode())
					user_id=user_df[user_df.apply(lambda x: x['email_id']==email_id.decode() and x['password']==password.decode(),axis=1)]["user_id"][0]
					break
		elif message==MENU or message==CHECK_FLIGHTS or message==VIEW_FLIGHT:
			clientsocket.send("OK".encode())

		elif message==BOOK_TICKETS:
			flight_number,number_of_seats = clientsocket.recv(50).decode().split()
			number_of_seats=int(number_of_seats)
			flight_df=pandas.DataFrame.from_csv("data/flights_details.csv")
			flight_df=flight_df[flight_df.apply(lambda x: x["flight_number"]==flight_number,axis=1)]
			depart_code=flight_df.iloc[0]["depart_code"]
			dest_code=flight_df.iloc[0]["dest_code"]
			journey_time=flight_df.iloc[0]["time"]
			user_bookings=pandas.DataFrame.from_csv("data/user_bookings/%s.csv"%user_id)
			count=0
			for i in range(number_of_seats):
				df=pandas.DataFrame.from_csv("data/flights/%s.csv"%flight_number)
				seat_number=clientsocket.recv(50).decode()
				seat_number=int(seat_number)
				if df["booking_status"][seat_number]!="not_booked" or flight_number in list(user_bookings.flight_number.dropna()):
					clientsocket.send("0".encode())
				else:
					count+=1
					df=df.set_value(seat_number-1,"booking_status","booked")
					df=df.set_value(seat_number-1,"user_id",user_id)
					df.to_csv("data/flights/%s.csv"%flight_number)
					clientsocket.send("1".encode())
			if count>0:
				user_bookings=user_bookings.append(pandas.DataFrame({"depart_code":[depart_code],"dest_code":[dest_code],"flight_number":[flight_number],"journey_time":[journey_time],"number_of_seats":[count]}))
				user_bookings.to_csv("data/user_bookings/%s.csv"%user_id)		
				
		elif message==ORDER_HISTORY:
			clientsocket.send(str(user_id).encode())

		elif message==CANCEL_TICKETS:
			flight_number,number_of_seats=clientsocket.recv(50).decode().split()
			user_bookings=pandas.DataFrame.from_csv("data/user_bookings/%s.csv"%user_id)
			count=0
			for t in range(int(number_of_seats)):
				df=pandas.DataFrame.from_csv("data/flights/%s.csv"%flight_number)
				seat_number=clientsocket.recv(50).decode()
				seat_number=int(seat_number)
				if df[df.apply(lambda x: x["seat_number"]==seat_number and x["user_id"]==str(user_id),axis=1)].empty:
					clientsocket.send("0".encode())
				else:
					df=df.set_value(seat_number-1,"booking_status","not_booked")
					df=df.set_value(seat_number-1,"user_id","null")
					df.to_csv("data/flights/%s.csv"%flight_number)
					count+=1
					clientsocket.send("1".encode())
			if user_bookings.apply(lambda x: x["flight_number"]==flight_number and x["number_of_seats"]==count,axis=1).any():
				user_bookings=user_bookings[user_bookings.apply(lambda x: x['flight_number']!=flight_number,axis=1)]
				user_bookings.to_csv("data/user_bookings/%s.csv"%user_id)
			else:

				df=user_bookings[user_bookings.apply(lambda x: x['flight_number']==flight_number,axis=1)]
				user_bookings=user_bookings[user_bookings.apply(lambda x: x['flight_number']!=flight_number,axis=1)]
				user_bookings=user_bookings.append(pandas.DataFrame({"depart_code":[df.iloc[0]["depart_code"]],"dest_code":[df.iloc[0]["dest_code"]],"flight_number":[flight_number],"journey_time":[df.iloc[0]["journey_time"]],"number_of_seats":[int(df.iloc[0]["number_of_seats"])-count]}))
				user_bookings.to_csv("data/user_bookings/%s.csv"%user_id)

		if flag==1:
			break 	 

	clientsocket.close()
	print("Client exited. Waiting for another client")
