from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    session,
    flash
)
from flask_mongoengine import MongoEngine
from config import Config ,email
import sys
from form import (CreatePatient, UpdatePatient, AddMedicine ,
 IssueMedicine123 , DiagnosticsFile, Issue_Diagnostics 
 , Pharmacy , Diagnostics,Bill , Admin_Reg, Admin_Log)
from model import Registration , Medicine, GiveMedicine,DiagnosticsMasterFile , IssueDiagnostics,Admin_Registration
from datetime import date,datetime 
import smtplib
import tkinter
from tkinter import messagebox


app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)


#--------------------------------------------Admin Register----------------------------------------
@app.route("/register",methods=['GET','POST'])
def admin_register():
	form = Admin_Reg()
	login_id = form.login_id.data
	pwd = form.pwd.data
	phn = str(form.phn_num.data)
	user_email=str(form.email.data)
	spl=["!","@","$","&","*","_","+","-","/","#","?"]
	if form.validate_on_submit():
		for i in list(spl):
			if i in pwd:
				f=0
				break
			else:
				f=1
		for j in range(0,len(pwd)):
			if pwd[j].isnumeric():
				num=0
				break
			else:
				num=1
		for k in range(0,len(pwd)):
			if pwd[k].isupper():
				up=0
				break
			else:
				up=1
		if len(login_id)<8: 
			flash("Login ID should be minimum of 8 characters long","danger")
		
		elif len(pwd) != 10:
			flash("Password must be exactly 10 characters long","danger")

		elif len(phn) != 10 :
			flash("Phone Number must be 10 digits","danger")
		
		elif not phn.isnumeric():
			flash("Phone Number should not contain Alphabets","danger") 

		elif f==1:
			flash("Password must contain a Special Character, like: '!','@','$','&','*','_','+','-','/','#','?'","danger")
		elif num==1:
			flash("Password must contain a Number","danger")
		elif up==1:
			flash("Password must contain an UpperCase Letter","danger")

		else:
			admin = Admin_Registration(login_id = login_id,email=user_email,phone_number=phn,timestamp = str(datetime.now()))
			admin.set_password(pwd)
			admin.save()
			flash("You have been Registered Successfully","success")
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email.EMAIL, email.EMAIL_PASSWORD)
			msg = "Thank You,You are successfully registered with ABC Hospital Management System.Your credentails are \n login_id is {} ,\n Your password is {}, \n Your Phone number is {},\n You are requested to keep this email for future usage".format(login_id,pwd,phn)
			server.sendmail(email.EMAIL, user_email, msg)
			flash("We have sent an Email with Login Credentials","success")
			
	return render_template("admin_registration.html",form = form)

#-------------------------------------------------------------------------------------------------------------
#----------------------------------------login----------------------------------------------------------------
@app.route("/",methods=['GET','POST'])
def admin_login():
	if session.get('login_id'):
		return redirect(url_for('welcome'))
	form = Admin_Log()
	login_id = form.login_id.data
	pwd = form.pwd.data
	check = Admin_Registration.objects(login_id = login_id).first()
	if form.validate_on_submit():
		if Admin_Registration.objects(login_id = login_id).first() and Admin_Registration.objects(login_id = login_id).first().get_password(pwd):
			session['login_id'] = login_id
			flash("Login Successful","success")
			return redirect(url_for('welcome'))
		elif Admin_Registration.objects(login_id = login_id).first() and pwd != Admin_Registration.objects(login_id = login_id).first().pwd :
			flash("The Password for the Login ID is incorrect","danger")
		else:
			flash("This is not a registered ID","danger")
			
			
	return render_template("admin_login.html",form = form)
#--------------------------------------------------------------------------------------

#-----------------------------------------logout---------------------------------
@app.route("/logout",methods=['GET','POST'])
def admin_logout():
    session['login_id']=False
    session.pop('login_id',None)
    return redirect(url_for('admin_login'))
#---------------------------------------------------------------------------------



 #------------------------------------------Home Page-------------------------------
@app.route("/welcome",methods=['GET','POST'])
def welcome():
	
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	return render_template('welcome.html')


#--------------------------------------------------------------------------


#______________________ Patient Registration __________________________

@app.route("/patRegistration",methods=['GET','POST'])
def patientRegistration():
	form =CreatePatient()
	patient_ssnid =form.patient_ssnid.data
	room_amount = 0
	
	if form.validate_on_submit():
		if Registration.objects(patient_ssnid=patient_ssnid):
			flash("A patient is already registered with this ID","danger")
		
		else:
			name = form.name.data
			age = form.age.data
			bedtype=str(dict(form.type_of_bed.choices).get(form.type_of_bed.data))
			if bedtype=="General Ward" : 
				room_amount=2000
			elif bedtype=="Sharing Ward":
				room_amount = 4000
			else:
				room_amount= 8000
			address=form.address.data
			doj=str(form.date_of_admission.data)
			state= str(dict(form.state.choices).get(form.state.data))
			city= str(dict(form.city.choices).get(form.city.data))
			if len(patient_ssnid)==9:
				patient= Registration(patient_ssnid=patient_ssnid,patient_name=name,
				age=age,bed_type=bedtype,address=address,state=state,city=city,doj=doj , room_amount = room_amount)
				patient.save()
				flash("Patient Registration Initiated Successfully","success") 
			else:
				flash("Patient SSNID should be exactly 9 digits","danger")
		
	return render_template("patientRegistration.html",form=form)

#____________________________________________________________________

#_______________________Update_______________________________________

@app.route("/updatepatient",methods=['GET','POST'])
def update_patient():
	form=UpdatePatient()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	patient_ssnid=form.patient_ssnid.data
	room_amount = 0
	pat = Registration.objects(patient_ssnid=patient_ssnid).first()
	bed_type=str(dict(form.type_of_bed.choices).get(form.type_of_bed.data))

	if form.get.data:
		if Registration.objects(patient_ssnid=patient_ssnid):
			flash("Patient Found","success")
			return redirect(url_for('fill_form',messages = patient_ssnid))
		else:
			flash("This ID is not registered","danger")

	return render_template("updatepatient.html",form=form,pat=pat)

@app.route("/fillform",methods=['GET','POST'])
def fill_form():
	
	form= UpdatePatient()
	ssnid = request.args['messages']
	room_amount = 0
	pat=Registration.objects(patient_ssnid=ssnid).first()
	
	form.patient_ssnid.data = ssnid
	if form.submit.data:
		if request.method == "POST":
			name = request.form["patientname"]
			age = request.form["age"]
			address = request.form["address"]
			#state = request.form["state"]
			#city = request.form["city"]
			state=str(dict(form.state.choices).get(form.state.data))
			city=str(dict(form.city.choices).get(form.city.data))
			bed_type=str(dict(form.type_of_bed.choices).get(form.type_of_bed.data))
			if bed_type=="General Ward" : 
				room_amount=2000
			elif bed_type=="Sharing Ward":
				room_amount = 4000
			else:
				room_amount= 8000
			Registration.objects(patient_ssnid=ssnid).update(patient_name=name,bed_type=bed_type,
			age=age,address=address,state=state,city=city, room_amount = room_amount)
			flash("Patient Update initiated successfully","success")
	return render_template("updatepatient.html",form=form,pat = pat)


#_____________________________________________________________________



#_______________________delete patient___________________________________________

@app.route("/deletepatient",methods=['GET','POST'])
def delete_patient():
	
	form= UpdatePatient()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	patient_ssnid=form.patient_ssnid.data
	pat = Registration.objects(patient_ssnid=patient_ssnid).first()
	bed_type=str(dict(form.type_of_bed.choices).get(form.type_of_bed.data))
	if form.get.data:
		if Registration.objects(patient_ssnid=patient_ssnid):
			flash("Patient Found","success")
			return redirect(url_for('fill_form1',msg = patient_ssnid))
		else:
			flash("This ID is not registered","danger")
		

	return render_template("deletepatient.html",form=form,pat=pat)

@app.route("/fillform1",methods=['GET','POST'])
def fill_form1():
	
	form= UpdatePatient()
	ssnid = request.args['msg']
	pat=Registration.objects(patient_ssnid=ssnid).first()
	form.patient_ssnid.data = ssnid
	bed_type=str(dict(form.type_of_bed.choices).get(form.type_of_bed.data))
	if form.delete.data:
			Registration.objects(patient_ssnid=ssnid).delete()
			GiveMedicine.objects(patient_ssnid=ssnid).delete()
			IssueDiagnostics.objects(patient_ssnid=ssnid).delete()
			flash("Patient Deletion Initiated Succefully","success")
	return render_template("deletepatient.html",form=form,pat = pat)

#___________________________________________________________________


#_________________________view Patient ______________________________

@app.route("/viewpatient",methods=['GET','POST'])
def view_patient():
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	view = Registration.objects().all()
	return render_template("viewpatient.html",view=view)
#_____________________________________________________________________


#________________________Search Patient ______________________________

@app.route("/searchpatient",methods=['GET','POST'])
def search_patient():
	
	form= UpdatePatient()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	patient_ssnid=form.patient_ssnid.data
	pat = Registration.objects(patient_ssnid=patient_ssnid).first()
	if form.get.data:
		if Registration.objects(patient_ssnid=patient_ssnid):
			flash("Patient Found","success")
			return fill_form2(patient_ssnid)
		else:
			flash("This ID is not registered","danger")

	return render_template("searchpatient.html",form=form,pat=pat)

def fill_form2(data):
	
	form= UpdatePatient()
	pat=Registration.objects(patient_ssnid=data).first()
	if form.submit.data:
		if request.method == "POST":
			name = request.form["patientname"]
			age = request.form["age"]
			address = request.form["address"]
			state = request.form["state"]
			city = request.form["city"]

			Registration.objects(patient_ssnid=data).update(patient_name=name,age=age,address=address,state=state,city=city)
			flash("Patient update initiated successfully","success")
	return render_template("searchpatient.html",form=form,pat = pat)

#______________________________________________________________________


#__________________________Add Medicine ____________________________

@app.route("/addmedicine",methods=["GET","POST"])
def add_medicine():
	form = AddMedicine()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	if form.validate_on_submit():
		id = form.med_id.data
		name = form.med_name.data
		quant = form.quant_available.data
		rate = form.rate.data
		if Medicine.objects(med_id = id) :
			flash("Medicine Already Exists","danger")
		else:
			med = Medicine(med_id = id, med_name = name, quant_available = quant , rate = rate )
			med.save()
			flash("Medicine is successfully Added to the Master File","success")

	return render_template("addmedicine.html",form = form)

#---------------------------------issue medicine--------------------------------
@app.route("/issuemedicine",methods=["GET","POST"])
def issue_medicine():
	
	amount=0
	form = IssueMedicine123()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	form.med_name1.choices=[(medicine.med_id,medicine.med_name) for medicine in Medicine.objects().all()]
	ssnid = form.patient_ssnid.data
	quant = form.quant.data
	if Registration.objects(patient_ssnid= ssnid):
			name= Medicine.objects(med_id=form.med_name1.data).first().med_name
			#if Medicine.objects(med_name = name):
			if Medicine.objects(med_name = name).first().quant_available >=quant :
				amount =  Medicine.objects(med_name = name).first().rate * quant
				price =  Medicine.objects(med_name = name).first().rate 
				ismed = GiveMedicine(patient_ssnid = ssnid, med_name = name, quantity = quant , amount = amount,rate = price)
				ismed.save()
				Medicine.objects(med_name=name).update(quant_available = Medicine.objects(med_name=name).first().quant_available - quant)
				flash("Medicine is successfully Issued","success")

			else: 
				flash("This much quantity of Medicine is not available in the store","danger")


	return render_template("issuemedicine.html",form = form , amount=amount)

#------------------------------------------------------------------------------------------------


#-------------------------------------------------add diagnostics------------------------------
@app.route("/DiagnosticsMasterFile",methods=["GET","POST"])
def diagnostics_master_file():
	form = DiagnosticsFile()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	if form.validate_on_submit():
		diag_id = form.Diagnostics_id.data
		test_name = form.test_name.data
		rate = form.rate.data
		if DiagnosticsMasterFile.objects(test_name = test_name) or DiagnosticsMasterFile.objects(diag_id = diag_id):
			flash("This id/test is already in the Master File","danger")
		else: 
			dia = DiagnosticsMasterFile(diag_id=diag_id,test_name = test_name, rate = rate)
			dia.save()
			flash("This Diagnostic Test has been successfully added to the Master File","success")

	return render_template("diamasterfile.html",form = form)

#------------------------------------------------------------------------------------

#------------------------------------issue diagnostics---------------------------------
@app.route("/IssueDiagnostics",methods=["GET","POST"])
def issue_diagnostics():
	amount = 0
	form = Issue_Diagnostics()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	form.test_name1.choices=[(i.diag_id,i.test_name) for i in DiagnosticsMasterFile.objects().all()]
	
	
	ssnid = form.patient_ssnid.data
		
		#print(form.test_name1.choices)
	if Registration.objects(patient_ssnid= ssnid).first():
		test_name= DiagnosticsMasterFile.objects(diag_id=form.test_name1.data).first().test_name
		if DiagnosticsMasterFile.objects(test_name = test_name):
			amount = DiagnosticsMasterFile.objects(test_name = test_name).first().rate
			give_dia = IssueDiagnostics(patient_ssnid = ssnid,test_name = test_name , amount = amount)
			give_dia.save()
			flash("The Diagnostics is issued to Patient","success")

	
	return render_template("issuedia.html",form = form, amount = amount)

#--------------------------------------------------------------------------------------

#--------------------------------Pharmacy-----------------------------------------------

@app.route("/pharmacy",methods=["GET","POST"])
def pharm():
	form = Pharmacy()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	acc=0
	ssnid = form.patient_ssnid.data
	print(ssnid)
	details = Registration.objects(patient_ssnid = ssnid)
	meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
	doj=""
#	amount=0
	if form.get.data:
		if  Registration.objects(patient_ssnid= ssnid).first():
					details = Registration.objects(patient_ssnid = ssnid)
					meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
					year_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[0:4]
					month_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[5:7]
					day_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[8:10]
					doj = day_doj+"-"+month_doj+"-"+year_doj
					flash("Patient Found","success")

		else : 
			flash("This ID is not registered","danger")

	elif request.method=="POST":
		
		ssnid = form.patient_ssnid.data
		if Registration.objects(patient_ssnid= ssnid):
			
			if 'update' in request.form:

				print("in loop")
				#print(ssnid)
				med=request.form[str(0)]
				quan=request.form[str(1)]
				rate=request.form[str(2)]
			
				if med=="" or quan=="" or rate=="":
					flash("Enter the values","danger")
				else:
					amount=int(quan)*int(rate)
					
					ismed = GiveMedicine(patient_ssnid = ssnid, med_name = med, quantity = quan , amount = amount,rate = rate)
					ismed.save()
					flash("The Medicine is added to the Patient","success")
	
	return render_template("pharmacy.html",form = form ,doj=doj
	, det = details , meds = meds_used,acc=1)

#----------------------------------------------------------------------------------


#-------------------------------------------Diagnostics--------------------------------------
@app.route("/diagnostics",methods=["GET","POST"])
def diagnostics():
	form = Diagnostics()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	ssnid = form.patient_ssnid.data
	details = Registration.objects(patient_ssnid = ssnid)
	test = IssueDiagnostics.objects(patient_ssnid = ssnid)
	doj=""
	#if form.validate_on_submit():
	if form.get.data:
		if Registration.objects(  patient_ssnid= ssnid):
				details = Registration.objects(patient_ssnid = ssnid)
				test = IssueDiagnostics.objects(patient_ssnid = ssnid)
				year_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[0:4]
				month_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[5:7]
				day_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[8:10]
				doj = day_doj+"-"+month_doj+"-"+year_doj
				flash("Patient Found","success")

		else : 
			flash("This ID is not registered","danger")

	elif request.method=="POST" :
		print("post")
		if Registration.objects(  patient_ssnid= ssnid):
			print("patient")
			if 'update' in request.form:
				print("update")
				name=request.form[str(0)]
				amount=request.form[str(1)]
				up=IssueDiagnostics(patient_ssnid=ssnid,test_name=name,amount=amount)
				up.save()
				flash("Diagnostics Test added Successfully to the Patient","success")


			
		
	return render_template("diagnostics.html",form = form ,doj=doj

	, det = details , tests = test)

#---------------------------------------------------------------------------------

#___________________________ Billing ____________________________________


mo=["Jan","Feb","Mar","Apr",""]

@app.route("/billing",methods=["GET","POST"])
def billing():
	form = Bill()
	if not session.get('login_id'):
		return redirect(url_for('admin_login'))
	test_sum=0
	med_sum=0
	doj=""
	dod=""
	calc=""
	room_calc=0
	ssnid = form.patient_ssnid.data
	#dod = form.dod.data
	details = Registration.objects(patient_ssnid = ssnid)
	test = IssueDiagnostics.objects(patient_ssnid = ssnid)
	for i in test:
		test_sum+=i.amount
	meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
	for k in meds_used:
		med_sum+=k.amount
	#if form.validate_on_submit():
	if form.get.data:
		if Registration.objects(patient_ssnid= ssnid).first():
			n= Registration.objects(patient_ssnid= ssnid).first()
			n=n.status
			if n=="Discharged":
					flash("The Patient is already Discharged","danger")
					dt=datetime.now()
					year=str(dt.year)
					month=str(dt.strftime("%m"))
					day=str(dt.day)
					year_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[0:4]
					month_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[5:7]
					day_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[8:10]
					dod = day+"-"+month+"-"+year
					doj = day_doj+"-"+month_doj+"-"+year_doj
					details = Registration.objects(patient_ssnid = ssnid)
					meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
					test = IssueDiagnostics.objects(patient_ssnid = ssnid)
					enter = datetime(int(year),int(month),int(day))
					leave = datetime(int(year_doj),int(month_doj),int(day_doj))
					calc = str(abs(leave - enter))[0:2]
					room_calc= int(calc) * Registration.objects(patient_ssnid = ssnid).first().room_amount
					return render_template('billing.html',form=form, det=details, med = meds_used ,n=n,
					test = test, test_sum = test_sum,med_sum=med_sum, tot = test_sum + med_sum + int(room_calc),dod=dod,
					doj = doj ,calc = calc, room_calc = room_calc)
			else:
				dt=datetime.now()
				year=str(dt.year)
				month=str(dt.strftime("%m"))
				day=str(dt.day)
				year_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[0:4]
				month_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[5:7]
				day_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[8:10]
				dod = day+"-"+month+"-"+year
				doj = day_doj+"-"+month_doj+"-"+year_doj
				details = Registration.objects(patient_ssnid = ssnid)
				meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
				test = IssueDiagnostics.objects(patient_ssnid = ssnid)
				enter = datetime(int(year),int(month),int(day))
				leave = datetime(int(year_doj),int(month_doj),int(day_doj))
				calc = str(abs(leave - enter))[0:2]
				room_calc= int(calc) * Registration.objects(patient_ssnid = ssnid).first().room_amount
				flash("Patient Found","success")
				return render_template('billing.html',form=form, det=details, med = meds_used ,
					test = test, test_sum = test_sum,med_sum=med_sum, tot = test_sum + med_sum + int(room_calc),dod=dod,
					doj = doj ,calc = calc, room_calc = room_calc)
		else:
			flash("This ID is not registered","danger")
	elif request.method=="POST":
		if Registration.objects(  patient_ssnid= ssnid):
			if 'confirm' in request.form:
				dt=datetime.now()
				year=str(dt.year)
				month=str(dt.strftime("%m"))
				day=str(dt.day)
				year_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[0:4]
				month_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[5:7]
				day_doj=str(Registration.objects(patient_ssnid = ssnid).first().doj)[8:10]
				dod = day+"-"+month+"-"+year
				doj = day_doj+"-"+month_doj+"-"+year_doj
				details = Registration.objects(patient_ssnid = ssnid)
				meds_used = GiveMedicine.objects(patient_ssnid = ssnid)
				test = IssueDiagnostics.objects(patient_ssnid = ssnid)
				enter = datetime(int(year),int(month),int(day))
				leave = datetime(int(year_doj),int(month_doj),int(day_doj))
				calc = str(abs(leave - enter))[0:2]
				room_calc= int(calc) * Registration.objects(patient_ssnid = ssnid).first().room_amount
				flash("The Patient Can Be Discharged","success")
				Registration.objects(patient_ssnid = ssnid).update(status = "Discharged")
				return render_template('billing.html',form=form, det=details, med = meds_used ,
					test = test, test_sum = test_sum,med_sum=med_sum, tot = test_sum + med_sum + int(room_calc),dod=dod,
					doj = doj ,calc = calc, room_calc = room_calc)
	return render_template('billing.html',form=form, det=details, med = meds_used , 
	test = test ,test_sum = test_sum,med_sum=med_sum,  tot = test_sum + med_sum +int(room_calc),dod=dod,
	doj = doj,calc = calc, room_calc = room_calc)

#----------------------------------------------------------------------------------------------
