from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField 
	, IntegerField,DateField,TextAreaField,SelectField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError,email_validator
from wtforms.fields.html5 import EmailField 
#import email_validator

states = [("1","Andhra Pradesh (Hyderabad)"), 
		("2","Arunachal Pradesh (Itanagar)"),
    	("3","Assam (Dispur)"),
    	("4","Bihar (Patna)"),
    	("5","Chhattisgarh (Raipur)"),
    	("6","Goa (Panaji)"),
    	("7","Gujarat (Gandhinagar)"),
    	("8","Haryana (Chandigarh)"),
	    ("9","Himachal Pradesh (Shimla)"),
	    ("10","Jharkhand (Ranchi)"),
	    ("11","Karnataka (Bangalore)"), 
	    ("12","Kerala (Thiruvananthapuram)"),
	    ("13","Madhya Pradesh (Bhopal)"),
	     ("14","Maharashtra (Mumbai)"),
	     ("15","Manipur (Imphal)"),
	     ("16","Meghalaya (Shillong)"),
	     ("17","Mizoram (Aizawl)"),
	     ("18","Nagaland (Kohima)"),
	     ("19","Odisha (Bhubaneshwar)"),
	     ("20","Punjab (Chandigarh)"),
	     ("21","Rajasthan (Jaipur)"),
	     ("22","Sikkim (Gangtok)"),
	     ("23","Tamil Nadu (Chennai)"),
	     ("24","Telangana (Hyderabad)"),
	     ("25","Tripura (Agartala)"),
	     ("26","Uttarakhand (Dehradun)"),
	     ("27","Uttar Pradesh (Lucknow)"),
	     ("28","West Bengal (Kolkata)")]

cities = [("1","Visakhapatnam"),
		  ("2","Bhismaknagar"),
		  ("3","Guwahti"),
		  ("4","Bilaspur"),
		  ("5","Margoa"),
		  ("6","Ahmedabad"),
		  ("7","faridabad"),
		  ("8","Dharmashala"),
    	  ("9","Jamshedpur"),
    	  ("10","Mysore"),
    	  ("11","Kochi"),
    	  ("12","Indore"),
    	  ("13","Pune"),
    	  ("14","Bishnupur"),
    	  ("15","Cherrapunji"),
    	  ("16","Tuensang"),
    	  ("17","Puri and Sambalpur"),
    	  ("18","Amritsar"),
    	  ("19","Jaisalmer"),
    	  ("20","Gyalshing"),
    	  ("21","Tiruchirappalli"),
    	  ("22","Karimnagar"),
    	  ("23","Udaipur"),
    	  ("24","Noida"),
    	  ("25","Haridwar"),
    	  ("26","Darjeeling")]

#-------------------------------------------Admin Login----------------------------------------
class Admin_Log(FlaskForm):
	login_id = StringField("Login ID",validators=[DataRequired(),], render_kw={"placeholder":"Login ID"})
	pwd = PasswordField("Password" , validators=[DataRequired()], render_kw={"placeholder":"Password"})
	login = SubmitField("Login")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Admin Registration----------------------------------------
class Admin_Reg(FlaskForm):
	login_id = StringField("Login ID",validators=[DataRequired()], render_kw={"placeholder":"Login ID"})
	pwd = StringField("Password" , validators=[DataRequired()], render_kw={"placeholder":"Password"})
	phn_num = StringField("Phone Number", validators=[DataRequired()], render_kw={"placeholder":"Phone Number"})
	email = EmailField('Email Address', validators=[DataRequired(), Email()])
	register = SubmitField("Register")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Create Patient----------------------------------------
class CreatePatient(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired()], render_kw={"placeholder":" SSN ID"})
		name = StringField("Patient Name",validators=[DataRequired()], render_kw={"placeholder":" Name"})
		age = IntegerField("Age",validators=[DataRequired()],render_kw={"placeholder":"Age"})
		date_of_admission =DateField('Date Of Admission *', format="%m/%d/%Y")
		type_of_bed = SelectField("Type",choices=[('1','General Ward'),('2','Sharing Ward'),('3','Single Room')], validators=[DataRequired()])
		address = TextAreaField("Address",validators=[DataRequired()],render_kw={"placeholder":"Address"})
		state = SelectField("State",choices=states,validators=[DataRequired()])
		city = SelectField("City",choices=cities,validators=[DataRequired()])
		submit =SubmitField("Submit")
#--------------------------------------------------------------------------------------------		
		
#-------------------------------------------Update Patient----------------------------------------
class UpdatePatient(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})
		get = SubmitField("GET")
		name = StringField("Patient Name",render_kw={"placeholder":" Name"})
		#state = StringField("State",render_kw={"placeholder":" Name"})
		age = IntegerField("Age",render_kw={"placeholder":"Age"})
		#city = StringField("City",render_kw={"placeholder":" Name"})
		state = SelectField("State",choices=states,validators=[DataRequired()])
		city = SelectField("City",choices=cities,validators=[DataRequired()])
		#date_of_admission 
		type_of_bed = SelectField("Type",choices=[('1','General Ward'),('2','Sharing Ward'),('3','Single Room')])
		address = TextAreaField("Address",render_kw={"placeholder":"Address"})
		submit =SubmitField("Submit")
		delete = SubmitField("Delete")
		bed_del = StringField("Type")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Add Medicine----------------------------------------
class AddMedicine(FlaskForm):
		med_id = IntegerField("ID",validators=[DataRequired()],render_kw={"placeholder":" ID"})
		med_name = StringField("Name", validators=[DataRequired()],render_kw={"placeholder":" Name"})
		quant_available = IntegerField("Quantity Available",validators=[DataRequired()],render_kw={"placeholder":" Quantity Available"})
		rate = IntegerField("Rate",validators=[DataRequired()],render_kw={"placeholder":" Rate"})
		submit = SubmitField("Submit")

#--------------------------------------------------------------------------------------------
#-------------------------------------------Issue Medicine----------------------------------------
class IssueMedicine123(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})
		med_name = StringField("Name",render_kw={"placeholder":" Name"})
		med_name1=SelectField("Medicine" ,choices=[],render_kw={"placeholder":" Select Medicine"})
		quant = IntegerField("Quantity",validators=[DataRequired()],render_kw={"placeholder":" Quantity"})
		amount = IntegerField("Amount",render_kw={"placeholder":" Rate"})
		submit = SubmitField("Issue")

#--------------------------------------------------------------------------------------------
#-------------------------------------------Add Diagnostics----------------------------------------
class DiagnosticsFile(FlaskForm):
		Diagnostics_id=IntegerField("ID",validators=[DataRequired()])
		test_name = StringField("Name", validators=[DataRequired()],render_kw={"placeholder":" Name"})
		rate = IntegerField("Price",render_kw={"placeholder":" Rate"})
		submit = SubmitField("Submit")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Issue Diagnostics----------------------------------------	
class Issue_Diagnostics(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})
		#test_name = StringField("Test Name", validators=[DataRequired()],render_kw={"placeholder":" Name"})
		test_name1 = SelectField("Test", choices=[],render_kw={"placeholder":" Select Medicine"})
		amount = IntegerField("Amount",render_kw={"placeholder":" Rate"})
		issue = SubmitField("Issue")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Pharmcy ----------------------------------------	
class Pharmacy(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})		
		get = SubmitField("GET")
#--------------------------------------------------------------------------------------------		
	
#-------------------------------------------Diagnostics File----------------------------------------	
class Diagnostics(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})		
		get = SubmitField("GET")
		issuedia = SubmitField("Add Diagnostics")
		update = SubmitField("Update")
#--------------------------------------------------------------------------------------------

#-------------------------------------------Billing----------------------------------------
class Bill(FlaskForm):
		patient_ssnid = StringField("Patient SSN ID",validators=[DataRequired(),Length(min=9,max=9)], render_kw={"placeholder":" SSN ID"})
		#dod = StringField("Date of Discharge", validators=[DataRequired()], render_kw={"placeholder":"dd-MON-yy"})
		get = SubmitField("GET")
		confirm = SubmitField("Confirm")
#--------------------------------------------------------------------------------------------		