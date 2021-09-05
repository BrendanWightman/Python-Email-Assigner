import smtplib
import imaplib
import random
from email.message import EmailMessage
from datetime import date

## Variable Setup Start

# Login Info (Change later)
Email = input("Enter Login Email: ")
Pass = input("Enter Login Password: ")

# iMap Info
imap_host = 'imap.gmail.com'

# Addr to send to
contacts = ['wightmannewsletter@gmail.com', 'wightmanbrendan@gmail.com', 
'bwightma@kent.edu', 'little.red.rose17@gmail.com']


#eFile = open("Payload.txt", 'r')
eFile = open("test.html", 'r')
emailMsg = eFile.read()

## Variable Setup End

## Functions`	

# I didn't feel like building an entire html parser so
# this parses based off of special comments
def createTask(eMail, addition):

    # 'parse' 
	htmlStEnd = eMail[eMail.rfind('<!-- START -->'):eMail.rfind('<!-- END -->') + 13]

	# Check if already in list
	if(eMail.find('<!-- TASKSTART -->' + addition) != -1 or eMail.find('<!-- TASKSTART --> ' + addition) != -1):
		toReplace = eMail[eMail.find('<!-- STATUSSTART -->') + 20 : eMail.find('<!-- STATUSEND -->')]
		eMail = eMail.replace(toReplace, 'Complete')
		#TODO Change color of status, correctly set date

		# Set Date
		today = date.today()
		toReplace = htmlStEnd[htmlStEnd.find('<!-- DATESTART -->') + 18 : htmlStEnd.find('<!-- DATEEND -->')]
		eMail = htmlStEnd.replace(toReplace, today.strftime("%m/%d/%y")) 
		return eMail

    # Set Task
	toReplace = htmlStEnd[htmlStEnd.find('<!-- TASKSTART -->') + 18 : htmlStEnd.find('<!-- TASKEND -->')]
	htmlStEnd = htmlStEnd.replace(toReplace, addition)

    # Set Name
	toReplace = htmlStEnd[htmlStEnd.find('<!-- NAMESTART -->') + 18 : htmlStEnd.find('<!-- NAMEEND -->')]
	coinFlip = 'Ally' if random.randrange(2) == 0 else 'Brendan'
	htmlStEnd = htmlStEnd.replace(toReplace,coinFlip)

    # Set Status
	toReplace = htmlStEnd[htmlStEnd.find('<!-- STATUSSTART -->') + 20 : htmlStEnd.find('<!-- STATUSEND -->')]
	htmlStEnd = htmlStEnd.replace(toReplace, 'Incomplete') 
    
	finalMsg = emailMsg[:emailMsg.rfind('<!-- END -->') + 13] + htmlStEnd
	return finalMsg

def sendEmail(message):

	msg = EmailMessage()
	msg['Subject'] = 'Current To-Do List'
	msg['From'] = Email
	msg['To'] = 'wightmannewsletter@gmail.com'
	#msg['To'] = ",".join(contacts)

	msg.set_content('Daily To Do')

	msg.add_alternative(message, subtype='html')

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(Email, Pass)
		smtp.send_message(msg)
		smtp.quit()

def stripMessage(message):
	message = message.replace('\\r', '')
	message = message.replace('\\n\\n', '')
	message = message.split('\\n')
	return message

## Functions End

## Imap stuff

# connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)

## login to server
imap.login(Email, Pass)

imap.select('Inbox')

_, data = imap.search(None, 'ALL')
for num in data[0].split():
	_, data = imap.fetch(num, '(RFC822)')
	print('Message: {0}\n'.format(num))
	eDataStr = str(data[0][1])

	oldMessage = ""
	# Save the current list as Payload.txt
	if(eDataStr.find('From: wightmannewsletter@gmail.com') != -1):
		oldMessage = eDataStr[eDataStr.find("<!DOCTYPE html>"):eDataStr.find("</html>")]
		oldMessage = oldMessage.replace('\\r\\n', '\n')
		with open('Payload.txt', 'w') as f:
			f.write(oldMessage)
	
	# Checks if from one of the contacts then inserts the new elements
	for word in eDataStr.split():
		if(word in contacts):
			# Find the correct spot to insert
			temp = stripMessage(eDataStr[eDataStr.find("Content-Type: text/plain; charset=\"UTF-8\"") + 41: eDataStr.find('--', eDataStr.find("Content-Type: text/plain; charset=\"UTF-8\""))])
			for ele in temp:
				emailMsg = createTask(emailMsg, ele)
			break

# For testing purposes only
with open('tmpF.html', 'w') as f:
	f.write(emailMsg)


#sendEmail(emailMsg)
#imap.store(num, '+FLAGS', '\\Deleted')
#imap.expunge()
imap.close()

## TO-Do:
# set some items on schedule, send email to contacts, 
# completed category, rollover from one day to the next, add error handling, weather reports,
# turn on a/c
