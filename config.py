import os
#py -c "import os; print(os.urandom(16))"
class email(object):
		
	EMAIL="your email id here"
	EMAIL_PASSWORD="email_id password"

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY") or b'\x1d\xe6\xf23=\xebr\x9a\xf17\xb8<4\x08\x9cf'

    MONGODB_SETTINGS = { 'db' : 'Hospital_Management'}
