# Database config
DATABASE_URL = "sqlite://"

TWILIO_ACCOUNT_SID = "AC3813535560204085626521"
TWILIO_ACCOUNT_AUTH_TOKEN = "2flnf5tdp7so0lmfdu3d7wod"
TWILIO_FROM_NUMBER = ""

AWS_REGION = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
EMAIL_SENDER = ""

SECRET_KEY = 'This is not secret you must change it'
HOST_NAME = 'http://localhost:4302'

BROKER = "sqla+%s" % DATABASE_URL
