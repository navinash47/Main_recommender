import mysql.connector
import pandas as pd
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="hospitals"
)
mycursor = mydb.cursor()
hosp_df=pd.read_csv("hospitals.csv")

for i,row in hosp_df.iterrows():

    val=(str(row["Place_1"]),str(row["Place_2"]),str(row["Name"]),str(row["Latitude"]),str(row["Longitude"]),str(row["Rating"]),str(row["Vicinity"]),str(row["Place_id"]),str(row["Open_Status"]),str(row["Phone_number"]),str(row["Dept"]),str(row["no_of_beds"]))
    sql="INSERT INTO hospitals(`Place_1`, `Place_2`, `NameOfHosp`, `Latitude`, `Longitude`, `Rating`, `Vicinity`, `Place_id`, `Open_Status`, `Phone_number`, `Dept`, `no_of_beds`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,val)
    mydb.commit()
    #print(val)


