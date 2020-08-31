import pandas
df={"first_name":[],"last_name":[],"email_id":[],"password":[],"phone_number":[],"dob":[],"user_id":[]}
df=pandas.DataFrame(df)
df.to_csv("user_data.csv",index=False)
