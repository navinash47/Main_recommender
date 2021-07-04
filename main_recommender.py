from numpy.core.numeric import NaN


def main_recomm( gender2,age,BT,PR,BOL,SBP,DBP,geo_lat,geo_lon):
    # imports
    import numpy as np
    import pickle
    import json
    try:
        import pandas as pd
    except Exception as e:
        print(e.__repr__())

    #get patients data as input
    # from find_hospitals import Patients_data

    #open model pickle
    pickle_in=open("model.pickle","rb")
    ml_model=pickle.load(pickle_in)
    
    if(gender2=='Male' or gender2=='male'):
        gender=1
    else:
        gender=0

    pred_args=[age,gender,BT,PR,BOL,SBP,DBP]
    pred_args_arr=np.array(pred_args)
    pred_args_arr=pred_args_arr.reshape(1,-1)

    #Writing predicted Critical Index value
    model_prediction=ml_model.predict(pred_args_arr)
    model_prediction=round(float(model_prediction),2)

    from functions_for_recomm import haversine,check_dept,cosine_similarity,euclid_similarity,Sum,normalize,send_out_data

    #Fetch all hospitals
    # d=Hosp_fetch()
    d=pd.read_csv("hospitals.csv")
 
    #finding hospitals in radius of 5 km 
    center_point = [{'lat': geo_lat, 'lng': geo_lat}]
    radius = 5.00 # in kilometer
    # hosp=pd.DataFrame(columns=["Name","Rating","Dept","Lat","Lon","Place_id","nob","Dis"])
    hosp=pd.DataFrame(columns=["Place_1","Place_2","Name","Latitude","Longitude","Rating","Vicinity","Place_id","Open_Status","Phone_number","Dept","no_of_beds","Dis"])
    

    dis=[]
    for index,row in d.iterrows():
        lat2=float(row["Latitude"])
        lon2=float(row["Longitude"])
        #assertion of point present within the radius
        a = haversine(geo_lon, geo_lat, lon2, lat2)
        if(a<=radius):
            hosp=hosp.append(row, ignore_index=True)
            dis.append(a)
    hosp["Dis"]=dis

    # sort according to required departments 
    medium_ci=["public health","nan","general practice","general surgery"]
    high_ci=["cardiology","cardiothoracic surgery","cardiovascular surgery","intensive care medicine","specialty"]
    # hosp1=pd.DataFrame(columns=["Name","Rating","Dept","Lat","Lon","Place_id","nob","Dis"])
    hosp1=pd.DataFrame(columns=["Place_1","Place_2","Name","Latitude","Longitude","Rating","Vicinity","Place_id","Open_Status","Phone_number","Dept","no_of_beds","Dis"])

    if float(model_prediction)<5:
        for index ,row in hosp.iterrows():         
            if check_dept(row,medium_ci):       
                hosp1=hosp1.append(row , ignore_index=True)
                    
    elif float(model_prediction)>=5:
        for index ,row in hosp.iterrows():
            if check_dept(row,high_ci):
                hosp1=hosp1.append(row , ignore_index=True)
    
    #sort according to Rating
    hosp1=hosp1.sort_values('Rating', ascending=False).drop_duplicates('Name')
    hosp1=hosp1.sort_values('Rating', ascending=False).drop_duplicates('Place_id')
    
    rating=hosp1["Rating"]
    nob=hosp1["no_of_beds"]
    dis=hosp1["Dis"]

    rating=normalize(rating)
    nob=normalize(nob)
    dis=normalize(dis)

    hosp1["norm_Rating"]=rating
    hosp1["norm_nob"]=nob
    hosp1["norm_Dis"]=dis

    try:
        cal1=cosine_similarity(hosp1,[max(rating),max(nob),min(dis)])
        hosp2=hosp1
        hosp2["cosine"]=cal1
        hosp2=hosp2.sort_values('cosine', ascending=False)
    except:
        print("no Hospital1")
        json_dic={}
        json_a=[]
        json_dic={"error":True}
        json_a.append(json_dic)
        return json.dumps(json_a)

    # print(hosp2)
    # try:
    #     cal2=euclid_similarity(hosp1,[max(rating),max(nob),min(dis)])
    #     hosp3=hosp1
    #     hosp3["euclid"]=cal2
    #     hosp3=hosp3.sort_values('euclid', ascending=False)
    # except:
    #     print("no Hospitals2")
    #     json_dic={}
    #     json_a=[]
    #     json_dic={"error":True}
    #     json_a.append(json_dic)
    #     return json.dumps(json_a)

    
    try:
        return send_out_data(hosp2,model_prediction)
    except:
        print("no Hospitals3")
        json_dic={}
        json_a=[]
        json_dic={"error":True}
        json_a.append(json_dic)
        return json.dumps(json_a)

