from datetime import date, timedelta, datetime
from cmu_graphics import*
from PIL import Image

def drawCalendar(app, currentDate, dateList):
    drawLabel(getCurrentMonth(dateList[0].month) + " " + str(dateList[0].year), 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawRect(78, 156, 98, 624, fill=rgb(238, 241, 247))
    drawRect(78, 78, 1366, 78, fill=rgb(238, 241, 247))
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawLine(78, 156, 1366, 156, fill=rgb(217, 217, 217))
    for y in range(234, 769, 78):
        drawLine(158, y, 1366, y, fill=rgb(217, 217, 217))
    for x in range(176, 1200, 170):
        drawLine(x, 78, x, 780, fill=rgb(217, 217, 217))
    x = 91
    for dates in dateList:
        x += 170
        if dates == currentDate:
            drawLabel(getCurrentDay(dates.weekday()) + " " + str(dates.day), x, 117, fill=rgb(25, 25, 25), size=27, font='DM Sans')
        else:
            drawLabel(getCurrentDay(dates.weekday()) + " " + str(dates.day), x, 117, fill=rgb(92, 92, 93), size=27, font='DM Sans 36pt')
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1224, 13, height=52, width=128)
    drawLabel('New Task', 1298, 39, size=19, align='center', font='DM Sans 36pt')
    drawLabel('+', 1243, 41, size=28, font='DM Sans 36pt')
    drawTimes(app)

def drawTimes(app):
    times = ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM',
             '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM',
             '9 PM', '10 PM', '11 PM']
    for i in range(0+app.index, app.index+7):
        drawLabel(times[i], 130, 234 + (i-app.index)*78, size=12, fill=rgb(92, 92, 93), font='DM Sans 36pt')

def drawTaskPopUp(taskName):
    popUpMenu = Image.open('Images/popupmenu.png') # Image is shape from https://docs.google.com/presentation/u/1/
    drawImage(CMUImage(popUpMenu), 789, 13, width=422, height=385)
    drawLine(793, 78, 1207, 78, fill=rgb(217, 217, 217))
    drawLine(793, 333, 1207, 333, fill=rgb(217, 217, 217))
    drawLabel(taskName, 810, 46, align='left', size=35, font='DM Sans')
    drawLabel('Cancel', 1050, 364, fill=rgb(167, 173, 173), size=17, font='DM Sans')
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1095, 344, height=40, width=98)
    drawLabel('Schedule', 1144, 364, size=17, font='DM Sans')
    drawLabel('Single event', 840, 105, align='left', size=20, font='DM Sans', fill=rgb(167, 173, 173))

def drawCheckBox(boxChecked):
    if boxChecked:
        drawRect(810, 95, 20, 20, fill=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'))
        check = Image.open('Images/check.png') # Icon from https://www.flaticon.com/free-icon/check_3388530?term=check+mark&page=1&position=5&origin=search&related_id=3388530
        drawImage(CMUImage(check), 820, 105, height=18, width=18, align='center')
    else:
        drawRect(810, 95, 20, 20, fill=None, border=rgb(217, 217, 217))

def drawSingleEventMenu(startTime, endTime, currentDate, buttonNum, rect1Fill, rect2Fill):
    drawRect(810, 135, 130, 40, fill=rect1Fill)
    drawLabel(startTime, 875, 155, size=30, font='DM Sans')
    drawLabel('to', 960, 155, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawRect(980, 135, 130, 40, fill=rect2Fill)
    drawLabel(endTime, 1045, 155, size=30, font='DM Sans')
    drawLabel('on', 1134, 159, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawDateButtons(810, 195, currentDate, buttonNum)

def checkDayButtonPresses(app, mouseX, mouseY, coords):
    buttonValue = 0
    for (x, y) in coords:
        if x <= mouseX <= x+90:
            if y <= mouseY <= y+50:
                if app.clickedDayButton == buttonValue:
                    app.clickedDayButton = 9
                else:
                    app.clickedDayButton = buttonValue
        buttonValue += 1

def checkStartEndTimePresses(app, mouseX, mouseY):
    if 810 <= mouseX <= 940:
        if 135 <= mouseY <= 175:
            app.rect1TextField = True
        else:
            app.rect1TextField = False
    else:
        app.rect1TextField = False
    if 980 <= mouseX <= 1115:
        if 135 <= mouseY <= 175:
            app.rect2TextField = True
        else:
            app.rect2TextField = False
    else:
        app.rect2TextField = False

def checkTextFieldLegality(app):
    if '|' in app.startTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.startTime, timeFormat)
    except ValueError:
        app.rect1Fill = rgb(255, 204, 203)
    ##############################################################################################
    if '|' in app.endTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.endTime, timeFormat)
    except ValueError:
        app.rect2Fill = rgb(255, 204, 203)
    ##############################################################################################

def checkDeadlineLegality(app):
    if '|' in app.deadline:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    try:
        currentTime = datetime.strptime(app.deadline, timeFormat)
    except ValueError:
        app.deadlineFill = rgb(255, 204, 203)

def isLegalTime(app):
    startTime = app.startTime.replace('|', '')
    endTime = app.endTime.replace('|', '')
    startTime = datetime.strptime(startTime, '%I:%M%p')
    endTime = datetime.strptime(endTime,'%I:%M%p')
    if app.selectedDate == app.currentDate:
        if startTime.time() >= app.currentTime.time() and endTime.time() > app.currentTime.time():
            return True
        return False
    else:
        return startTime.time() < endTime.time()
    
def isLegalDeadline(app):
    if app.selectedDate == app.currentDate:
        time = app.deadline.replace('|', '')
        deadlineTime = datetime.strptime(time, '%I:%M%p')
        if (deadlineTime-timedelta(hours=app.durationHours, minutes=app.durationMinutes)).time() <= app.currentTime.time():
            app.deadlineFill = rgb(255, 204, 203)
            return False
    return True

def checkInTextField(app):
    if app.taskNameTextField:
        if app.cursorTimer == 8 and (app.taskName == '' or app.taskName[-1] != '|'):
            app.taskName += '|'
        app.cursorTimer += 1
        if app.cursorTimer == 16:
            app.cursorTimer = 0
            app.taskName = app.taskName.replace('|', '')
    else:
        if 8 <= app.cursorTimer <= 15 and '|' in app.taskName:
            app.taskName = app.taskName[:-1]
            app.cursorTimer = 0
    if app.singleEventChecked:
        if app.rect1TextField:
            app.rect1Fill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.startTime == '' or app.startTime[-1] != '|'):
                app.startTime += "|"
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.startTime = app.startTime.replace('|', '')
        else:
            if app.startTime != '' and app.startTime[-1] == '|':
                app.startTime = app.startTime[:-1]
                app.cursorTimer = 0
        if app.rect2TextField:
            app.rect2Fill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.endTime == '' or app.endTime[-1] != '|'):
                app.endTime += "|"
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.endTime = app.endTime.replace('|', '')
        else:
            if app.endTime != '' and app.endTime[-1] == '|':
                app.cursorTimer = 0
                app.endTime = app.endTime[:-1]
    else:
        if app.deadlineTextField:
            app.deadlineFill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.deadline == '' or app.deadline[-1] != '|'):
                app.deadline += '|'
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.deadline = app.deadline.replace('|', '')
        else:
            if app.deadline != '' and app.deadline[-1] == '|':
                app.cursorTimer = 0
                app.deadline = app.deadline[:-1]

def drawDateButtons(startX, startY, currentDate, buttonNum):
    x = startX
    y = startY
    for nums in range(0, 8):
        if nums == buttonNum:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
        else:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173))
        nextDate = currentDate + timedelta(days=nums)
        if nextDate not in app.dayButtonList:
            app.dayButtonList.append(nextDate)
        drawLabel(str(nextDate.month) + '/' + str(nextDate.day), x+45, y+25, fill='white', size=15, font='DM Sans')
        x += 95
        if x == 1190:
            x = startX
            y += 55

def drawMultipleEventsMenu(deadline, hours, minutes, currentDate, buttonNum, deadlineFill, plusOpacity, minusOpacity):
    drawLabel('Duration', 810, 142, fill=rgb(167, 173, 173), size=25, align='left', font='DM Sans')
    drawRect(1000, 142, 163, 30, fill=None, border=rgb(217, 217, 217), align='center')
    plus = Image.open('Images/add.png') # Icon from https://www.flaticon.com/free-icon/subtraction_4230191?term=minus&page=1&position=36&origin=search&related_id=4230191
    drawCircle(1063, 142, 12, align='center', fill=rgb(238, 241, 247), opacity = plusOpacity)
    drawImage(CMUImage(plus), 1063, 142, height=20, width=20, align='center')
    minus = Image.open('Images/subtraction.png') # Icon from https://www.flaticon.com/free-icon/add_992651?term=add&page=1&position=2&origin=search&related_id=992651
    drawCircle(938, 142, 12, align='center', fill=rgb(238, 241, 247), opacity=minusOpacity)
    drawImage(CMUImage(minus), 938, 142, height=24, width=24, align='center')
    if hours == 0:
        drawLabel(f'{minutes} min', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    elif minutes == 0:
        drawLabel(f'{hours} hrs', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    else:
        drawLabel(f'{hours} hrs {minutes} min', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    drawDateButtons(810, 211, currentDate, buttonNum)
    drawLabel('Deadline', 810, 185, fill=rgb(167, 173, 173), size=25, align='left', font='DM Sans')
    drawRect(973, 185, 110, 35, align='center', fill=deadlineFill)
    drawLabel(deadline, 973, 185, align='center', size=25, font='DM Sans')
    drawLabel('on', 1035, 188, align='left', fill=rgb(167, 173, 173), size=25, font='DM Sans')

def checkDeadlinePress(app, mouseX, mouseY):
    if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
        app.deadlineTextField = True
    else:
        app.deadlineTextField = False

def checkDurationPress(app, mouseX, mouseY):
    if 918 <= mouseX <= 1068 and 127 <= mouseY <= 157:
        app.durationTextField = True
    else:
        app.durationTextField = False

def getCurrentDay(number):
    if number == 0:
        return 'Mon'
    elif number == 1:
        return 'Tue'
    elif number == 2:
        return 'Wed'
    elif number == 3:
        return 'Thu'
    elif number == 4:
        return 'Fri'
    elif number == 5:
        return 'Sat'
    else:
        return 'Sun'
    
def getCurrentMonth(number):
    if number == 1:
        return 'January'
    elif number == 2:
        return 'February'
    elif number == 3:
        return 'March'
    elif number == 4:
        return 'April'
    elif number == 5:
        return 'May'
    elif number == 6:
        return 'June'
    elif number == 7:
        return 'July'
    elif number == 8:
        return 'August'
    elif number == 9:
        return 'September'
    elif number == 10:
        return 'October'
    elif number == 11:
        return 'November'
    else:
        return 'December'