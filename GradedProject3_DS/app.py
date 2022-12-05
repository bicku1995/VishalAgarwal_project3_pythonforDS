# importing necessary libraries and functions
import numpy as np
from flask import Flask, request, jsonify, render_template,session,url_for
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb'))
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/login'
app.config['SQLALCHEMY_MODIFICATIONS']=True
db=SQLAlchemy(app)
class Log(db.Model):   
    username = db.Column(db.String, unique=True, nullable=False)
    passcode = db.Column(db.Integer, primary_key=True)
@app.route('/Register.html',methods=["POST"])
def reg():
     if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        entry=Log(username=username,passcode=password)
        db.session.add(entry)
        db.session.commit()
        out="Username registered"
     return render_template('Register.html',msg=out)
    
app.secret_key="login"
@app.route('/') # Homepage
def home():
    return render_template('home.html')
@app.route('/Login.html') # Login page
def login1():
    return render_template('Login.html')
@app.route('/Predict.html') # Predict page
def predict():
    return render_template('Predict.html') 
@app.route('/Register.html') # Register page
def register():
    return render_template('Register.html')

@app.route('/Login.html',methods=["POST"]) 
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if(username=="Vishal" and password=="112233"):
            session['form']=username 
            return render_template('Predict.html',email=username)
        else:
            msg="Invalid username/password"
            return render_template('Login.html',msg=msg)     
@app.route('/Predict.html',methods=['POST'])
def predict1():
    if request.method=='POST':
        gender=str(request.form['gender'])
        married=str(request.form['married'])
        dependents=float(request.form['dependents'])
        education=str(request.form['education'])
        self_employed=str(request.form['self-employed'])
        applicantincome=int(request.form['Applicant Income ($)'])
        coapplicantincome=float(request.form['Coapplicant Income ($)'])
        loanammount=float(request.form['Loan Ammount ($)'])
        loan_ammount_term=float(request.form['Loan Ammount Terms (in months)'])
        credit_history=float(request.form['Credit History'])
        property_area=str(request.form['Property Area'])
        prediction=model.predict([[gender,married,dependents,education,self_employed,applicantincome,coapplicantincome,loanammount,loan_ammount_term,credit_history,property_area]])
        output=prediction
   

    if(output=="1"):
        return render_template('Predict.html', prediction_text='You are eligible for loan')
    else:
        return render_template('Predict.html', prediction_text='You are not eligible for loan')
        

if __name__ == "__main__":
    app.run(debug=True)