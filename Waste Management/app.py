from flask import Flask,request,render_template,redirect,jsonify
from os import environ 
app=Flask(__name__)
login_status=0
mla_name=''
mla_location=''
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/user')
def users():
    return render_template("user.html")
@app.route('/management')
def management_login():
    return render_template("login.html")

@app.route('/login' ,methods=['POST','GET'])
def login():
    global login_status
    global mla_name
    if request.method=='POST':
        username1=request.form['name']
        password1=request.form['password']
        file = open("Login.txt","r")
        for row in file:
            field = row.split(",")
            username = field[0]
            password = field[1]
            lastchar = len(password)-1
            password = password[0:lastchar]

            if username1 == username and password1 == password:
                login_status=1
                mla_name=field[0]
                print(mla_name)
                return redirect('/admin')
        return render_template("login.html",message="Invalid username or password")
@app.route('/register') 
def register():
    areas=["UDUPI","KARKALA","KAUP","BRAHMAVARA","KUNDAPUARA"]
    return render_template('register.html',areas=areas)
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
       SECRET_KEY = environ.get('MLA_ID')
       _id=request.form['_id']  
       if(SECRET_KEY== _id):
           username =request.form['name']
           password =request.form['password']
           email=request.form['email']
           phno=request.form['phno'] 
           area=request.form['area']
           file = open("Login.txt","a")
           file.write (username)
           file.write (",")
           file.write (password)
           file.write("\n")
           file.close()
           file = open("admin.txt","a")
           file.write (username)
           file.write (",")
           file.write (email)
           file.write (",")
           file.write (phno)
           file.write (",")
           file.write (area)
           file.write ("\n")
           file.close()
           return redirect('/management')
       else:
          return render_template('register.html',message="MLA_id is wrong....")           
@app.route('/request',methods=['POST','GET'])
def requested():
    if request.method=='POST':
       v_name=request.form['name']
       if request.form['email']=='undefined':
           v_email="not provided"
       else:
           v_email=request.form['email']
       v_phno=request.form['phno']
       v_area=request.form['area']
       mla=request.form['mla']
       v_address=request.form['address']
       t_place=request.form['t_place']
       t_city=request.form['t_city']
       t_pin=request.form['t_pin']
       t_landmark=request.form['t_landmark']
       t_condition=request.form['t_condition']
       address= v_address.replace('\n', ' ').replace('\r', '')
       v_address="".join(address)      
       file = open("cases.txt","a")
       file.write (v_name)
       file.write (",")
       file.write (v_email)
       file.write (",")
       file.write (v_phno)
       file.write (",")
       file.write (v_area)
       file.write (",")
       file.write (mla)
       file.write (",")
       file.write (v_address)
       file.write (",")
       file.write (t_place)
       file.write (",")
       file.write (t_city)
       file.write (",")
       file.write (t_pin)
       file.write (",")
       file.write (t_landmark)
       file.write (",")
       file.write(t_condition)
       file.write ("\n")
       file.close()
       return "request is sent successfully"
@app.route('/admin')
def management():
    global login_status
    global mla_name
    global mla_location
    file=open("admin.txt","r")
    for line in file.readlines():
        slis=[]
        slis=line.split(",")
        if(slis[0]==mla_name):
            temp=slis[3][:-1]
            mla_location=temp
            break
    if login_status==1:
        print(mla_location)
        main_lis=[]
        file=open("cases.txt","r")
        for line in file.readlines():
            lis=[]
            lis=line.split(",")
            if(lis[3]==mla_location):
                main_lis.append(lis)
            
        length=len(main_lis)    
        return render_template("management_portal.html",cases=main_lis,length=length)           
    else:
        return "<h1>404 Bad GateWay</h1>"     
@app.route('/logout')
def logout():
    global login_status
    login_status=0
    return redirect('/management')
@app.route('/details',methods=['POST','GET']) 
def details():
    address=request.form['address']
    add=list(address.split(" "))
    return render_template("details.html",detail=request.form,address=add)
        
if __name__=="__main__":
    app.run(debug=True)