import main
from flask_mongoengine import MongoEngine
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

class Admin_Registration(db.Document):
    login_id =  db.StringField(unique=True)
    pwd = db.StringField()
    phone_number = db.StringField(unique=True)
    email=db.StringField(default="0")
    timestamp = db.StringField(default = "0")


    def set_password(self, pwd):
        self.pwd = generate_password_hash(pwd)
    def get_password(self, pwd):
        return check_password_hash(self.pwd, pwd)    


class Admin_Login(db.Document):
    login_id =  db.StringField(unique=True)
    pwd = db.StringField()
    timestamp = db.StringField(default = "0")
    

class Registration(db.Document):
    patient_ssnid = db.StringField( unique=True )
    patient_name = db.StringField( max_length=50 )
    age = db.IntField()
    address =  db.StringField( max_length=100 )
    doj=db.StringField(default='0')
    bed_type=db.StringField()
    state = db.StringField()
    city = db.StringField()
    room_amount = db.IntField()
    status = db.StringField(default="In Patient")
   
class Medicine(db.Document):
    med_id = db.IntField(unique=True )
    med_name = db.StringField()
    quant_available = db.IntField()
    rate = db.IntField()

class GiveMedicine(db.Document):
    patient_ssnid = db.StringField()
    med_name = db.StringField(default="-")
    quantity = db.IntField()
    rate = db.IntField()
    amount = db.IntField()

class DiagnosticsMasterFile(db.Document):
    diag_id=db.IntField(unique=True)
    test_name = db.StringField()
    rate = db.IntField()

class IssueDiagnostics(db.Document):
    patient_ssnid = db.StringField()
    test_name = db.StringField()
    amount = db.IntField()