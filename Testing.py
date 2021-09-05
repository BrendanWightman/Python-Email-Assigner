import random
from datetime import date

def createTask(eMail, addition):
    # 'parse' 
    htmlStEnd = eMail[eMail.rfind('<!-- START -->'):eMail.rfind('<!-- END -->') + 13]
    
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

    # Set Date
    today = date.today()
    toReplace = htmlStEnd[htmlStEnd.find('<!-- DATESTART -->') + 18 : htmlStEnd.find('<!-- DATEEND -->')]
    htmlStEnd = htmlStEnd.replace(toReplace, today.strftime("%m/%d/%y"))  
    
    finalMsg = emailMsg[:emailMsg.rfind('<!-- END -->') + 13] + htmlStEnd + emailMsg[emailMsg.rfind('<!-- END -->'):]
    print(finalMsg)

eFile = open("Test.html", 'r')
emailMsg = eFile.read()

createTask(emailMsg, 'Mow Lawn')

    # taskStart = htmlStEnd[htmlStEnd.find('<!-- TASKSTART -->'):htmlStEnd.find('<!-- TASKEND -->') + 17]
	# dateStart = htmlStEnd[htmlStEnd.find('<!-- DATESTART -->'):htmlStEnd.find('<!-- DATEEND -->') + 17]
	# nameStart = htmlStEnd[htmlStEnd.find('<!-- NAMESTART -->'):htmlStEnd.find('<!-- NAMEEND -->') + 17]
	# statusStart = htmlStEnd[htmlStEnd.find('<!-- STATUSSTART -->'):htmlStEnd.find('<!-- STATUSEND -->') + 19]