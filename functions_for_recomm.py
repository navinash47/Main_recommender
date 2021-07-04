from math import radians, cos, sin, asin, sqrt
# import mysql.connector as mdb
import numpy as np
import os
import sys
import json
import pandas as pd
from scipy.spatial import distance

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def check_dept(Hospital,cond_dept):
    flag=False
    
    for dept in cond_dept:
        if dept in (str(Hospital["Dept"])).split(','): 
            
            flag=True
            break
    return flag

def cosine_similarity(calc,r):
    print("check")
    full=[]
    for index,row in calc.iterrows():
        full.append(1 - distance.cosine([row["norm_Rating"],row["norm_nob"],row["norm_Dis"]], r))
    print("check")
    return full

def euclid_similarity(calc,r):
    full=[]
    for index,row in calc.iterrows():
        full.append(distance.euclidean([row["norm_Rating"],row["norm_nob"],row["norm_Dis"]], r))
    return full

def Sum(attr):
    Sum=0
    for i in attr:
        if(i!="nan"):
            Sum=Sum+float(i)
    return Sum

def normalize(attr):
    norm_attr=[]
    s=Sum(attr)
    for i in attr:
        if(i=="nan"):
            norm_attr.append(0)
        else:
            norm_attr.append(float(i)/s)
    return norm_attr

def send_out_data(hosp,ci):


    json_a=[]
    no_of_hosp=hosp.shape[0]
    if(no_of_hosp==0):
        print("no Hospitals")
        json_dic={}
        json_dic={"error":True}
        json_a.append(json_dic)
    
    for index,row in hosp.iterrows():
        json_dic={}
        json_dic["error"]=False
        json_dic["phone"]=str(row["Phone_number"])
        json_dic["name"]=str(row["Name"])
        json_dic["Lat"]=str(row["Latitude"])
        json_dic["Lon"]=str(row["Longitude"])
        json_dic["nob"]=str(row["no_of_beds"])
        json_dic["noofhosp"]=str(no_of_hosp)
        json_dic["Rating"]=str(row["Rating"])
        json_dic["Department"]=str(row["Dept"])
        json_dic["ci"]=str(ci)
        print(json_dic)
        json_a.append(json_dic)
            
    # print(json_a)

    return json.dumps(json_a)


