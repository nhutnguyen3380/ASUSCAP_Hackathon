# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACb9b69fcad32c0d9fd02fea6c8fad4a70'
auth_token = '3b6f6fac6068b5abd5e255093fefea09'
client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+14015922644',
#                      to=''
#                 )
# print(message.sid)

#tutorial: https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python