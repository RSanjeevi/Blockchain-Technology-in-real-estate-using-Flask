import hashlib as hasher
import datetime as date
import pymysql
from flask import Flask,redirect,url_for,request,render_template
app=Flask(__name__)
username1=''
password1=''
@app.route('/register/',methods=['POST','GET'])
def register():
	if request.method=='POST':
		db=pymysql.connect("localhost","root","","blockchain")
		land_owner_name=request.form['land_owner_name']
		address=request.form['address']
		land_type=request.form['land_type']
		land_size=request.form['land_size']
		location=request.form['location']
		facilities=request.form['facilities']
		surrended_by=request.form['surrended_by']
		Aadhar_card_no=request.form['Aadhar_card_no']
		Original_land_value=request.form['Original_land_value']
		Land_value_after_bought=request.form['Land_value_after_bought']
		sha =hasher.sha256()
		global username1,password1
		h=username1+password1
		h=h.encode('utf-8')
		sha.update(h)
		Hash_value=sha.hexdigest()
		
		print(land_owner_name,address,land_type,land_size,facilities,surrended_by)
		cursor = db.cursor()
		
		# cursor.execute("INSERT INTO registered(owner_name,address, land_type, land_size, location, facilities, surrendedBy,Aadhar_card_no,Original_land_value,Original_land_value,usernname,password) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(str(land_owner_name),str(address),str(land_type),str(land_size),str(location),str(facilities),str(surrended_by),str(Aadhar_card_no),str(Original_land_value),str(Land_value_after_bought),str(username),str(password)))

		cursor.execute("UPDATE registered SET owner_name='{}',address='{}', land_type='{}', land_size='{}', location='{}', facilities='{}', surrendedBy='{}',Aadhar_card_no='{}',Original_land_value='{}',Land_value_after_bought='{}',Hash_value='{}' where usernname='{}' and password='{}'".format(str(land_owner_name),str(address),str(land_type),str(land_size),str(location),str(facilities),str(surrended_by),str(Aadhar_card_no),str(Original_land_value),str(Land_value_after_bought),str(Hash_value),str(username1),str(password1)))
		db.commit()
		return render_template("login.html")

	else:
		land_owner_name = request.args.get('land_owner_name')
		address = request.args.get('address')
		land_type=request.args.get('land_type')
		land_size=request.form['location']
		return land_owner_name,address,land_type,land_size



@app.route('/result',methods=['POST','GET'])
def login():
	if request.method=='POST':
		user=request.form['Username']
		password=request.form['Password']
		sha =hasher.sha256()
		
		h=user+password
		h=h.encode('utf-8')
		sha.update(h)
		Hash_value=sha.hexdigest()
		#username and password validation
		db=pymysql.connect("localhost","root","","blockchain")
		cursor = db.cursor()
		cursor.execute('select * from registered where Hash_value="{}"'.format(Hash_value))
		data=cursor.fetchall()
		table_name=['owner_name',' address', 'land_type',' land_size', 'location', 'facilities', 'surrendedBy','Aadhar_card_no','Original_land_value','Land_value_after_bought']
		if(len(data)!=0):
			return  render_template("result.html",result = data[0],table=table_name)
		else:
			return "password incorrect"
	else:
		user = request.args.get('Username')
		password = request.args.get('Password')
		return user,password



@app.route('/signup',methods=['POST','GET'])
def signup():
	if request.method=='POST':
		db=pymysql.connect("localhost","root","","blockchain")
		cursor = db.cursor()

		user=str(request.form['s_username'])
		password=request.form['s_password']
		global username1,password1
		username1=user
		password1=password
		cursor.execute("insert into registered(usernname,password) VALUES('{}','{}')".format(user,password))
		db.commit()
		return  render_template("register.html")
	else:
		user = request.args.get('Username')
		password = request.args.get('Password')
		return user,password

if __name__ == '__main__':

	# b
	app.run(debug = True)