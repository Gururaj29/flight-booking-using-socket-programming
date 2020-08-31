import pandas
df=pandas.DataFrame.from_csv('flights_details.csv')
flights=list(df.flight_number.dropna())
dataframe={"booking_status":[],"seat_number":[],"user_id":[]}
for i in range(1,53):
	dataframe["seat_number"].append(i)
	dataframe["booking_status"].append("not_booked")
	dataframe["user_id"].append("Null")
dataframe=pandas.DataFrame(dataframe)
for i in flights:
	dataframe.to_csv("flights/%s.csv"%i)
