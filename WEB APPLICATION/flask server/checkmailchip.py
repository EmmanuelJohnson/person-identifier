import smtplib
from email.mime.text import MIMEText

# Define to/from
def startda(subject,recipient,msgforemail):
	sender = 'bobbyda.16@gmail.com'


	# Create message
	msg = MIMEText(msgforemail)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = recipient

	# Create server object with SSL option
	server = smtplib.SMTP("smtp.mailgun.org", 587)
	server.ehlo()
	# Perform operations via server
	server.login('postmaster@sandboxcf10728931384945858879ffeed638ea.mailgun.org', '9fa1956843f1afe6881a7c8024963289')
	server.sendmail(sender, [recipient], msg.as_string())
	server.close()
