from flask import Flask,request,jsonify
#import mysql.connector as mdb
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def Recommender():
    if request.method =='POST':
        gender=request.form['Gender']
        age=float(request.form['Age'])
        BT=float(request.form['BT'])
        PR=float(request.form['PR'])
        BOL=float(request.form['BOL'])
        SBP=float(request.form['SBP'])
        DBP=float(request.form['DBP'])
        lat=float(request.form['Latitude'])
        lon=float(request.form['Longitude'])

        from main_recommender import main_recomm
        
        return main_recomm(gender,age,BT,PR,BOL,SBP,DBP,lat,lon)
    return jsonify({'ip': request.remote_addr}), 200
    
    #return "Falied somehow!"


if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0")

