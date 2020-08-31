import pandas
df={"flight_number":[],"destination":[],"dest_code":[],"departure":[],"depart_code":[],"time":[],"price":[]}
df["flight_number"]=["F1425","F1231","F1901","F2901","F7111","F9012","F7822","F1999","F0092","F6723","F8211","F1021"]
df["destination"]=["Bengaluru","Kolkata","Mumbai","Bengaluru","Delhi","Mumbai","Bengaluru","Kolkata","Kolkata","Delhi","Mumbai","Delhi"]
df["dest_code"]=["BEN","KOL","MUM","BEN","DEL","MUM","BEN","KOL","KOL","DEL","MUM","DEL"]
df["departure"]=["Kolkata","Delhi","Bengaluru","Mumbai","Bengaluru","Kolkata","Delhi","Bengaluru","Mumbai","Kolkata","Delhi","Mumbai"]
df["depart_code"]=["KOL","DEL","BEN","MUM","BEN","KOL","DEL","BEN","MUM","KOL","DEL","MUM"]
df["time"]=["23rd Nov 12:00","24th Nov 03:00","29th Nov 10:20","01th Dec 09:00","04th Dec 12:10","09th Dec 14:55","10th Dec 19:45","12th Dec 16:40","14th Dec 13:30","14th Dec 15:00","15th Dec 05:30","16th Dec 12:00"]
df["price"]=[7600,14000,20000,24000,13000,34000,2400,24000,12000,23000,1400,15000]
pandas.DataFrame(df).to_csv("flights_details.csv")
