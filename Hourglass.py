from datetime import date, timedelta, datetime
from cmu_graphics import*
from calendarScreen import*
from tasks import*
from habits import*
from stats import*
from PIL import Image
import csv
import random

def onAppStart(app):
    app.background = rgb(246, 248, 252)
    app.currentDate = date.today()
    app.currentTime = datetime.now()
    app.weeklyDateList = getDatesList(app.currentDate)
    app.weeklyEvents = dict()
    app.times = ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM',
             '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM',
             '9 PM', '10 PM', '11 PM', '12 AM']
    app.shownTimes = []
    app.index = 8
    app.taskName = 'Task name'
    app.habitName = 'Habit name'
    app.singleEventTasks = importSingleEventData()
    app.splitTasks = importSplitEventData()
    app.splitTaskWorkSessions = dict()
    app.habitsSet = importHabitData()
    app.taskNameTextField = False
    app.habitsNameTextField = False
    app.selectedHabitDays = set()
    app.habitsPopUp = False
    app.rect1TextField = False
    app.rect2TextField = False
    app.rect3TextField = False
    app.rect4TextField = False
    app.deadlineTextField = False
    app.deadlineFill = rgb(255, 255, 255)
    app.minusOpacity = 0
    app.plusOpacity = 0
    app.durationTextField = False
    app.cursorTimer = 8
    app.clickedDayButton = 9
    app.singleEventDayButtonList = createDateButtons(810, 195, app.currentDate, 0)
    app.splitEventDayButtonList = createDateButtons(810, 211, app.currentDate, 2)
    app.habitsButtonList = createDateButtons(810, 211, None, 0)
    app.dayButtonList = []
    app.selectedDate = None
    app.startTime = '12:00pm'
    app.endTime = '12:00am'
    app.habitStartTime = '12:00pm'
    app.habitEndTime = '12:00am'
    app.deadline = '12:00pm'
    app.durationMinutes = 15
    app.durationHours = 0
    app.rect1Fill = rgb(255, 255, 255)
    app.rect2Fill = rgb(255, 255, 255)
    app.rect3Fill = rgb(255, 255, 255)
    app.rect4Fill = rgb(255, 255, 255)
    app.colorPalette = ["251| 194| 194|", "203| 120| 118", "180| 207| 164", "98| 134| 108", "244| 211| 94",
                        "246| 123| 69", "100| 85| 123", "187| 166| 221", "160| 197| 227", "50| 118| 155"] # Colors sourced from https://i.pinimg.com/736x/af/34/ec/af34ec62e403206b0c9fce24051f9160.jpg
    app.calendar = True
    app.taskPopUp = False
    app.singleEventChecked = False
    app.tasks = False
    app.habits = False
    app.stats = False
    app.timeDelta = 0
    app.calendarButtonOpacity = 0
    app.tasksButtonOpacity = 0
    app.habitsButtonOpacity = 0
    app.statsButtonOpacity = 0
    app.onCalendarButton = False
    app.onTasksButton = False
    app.onHabitsButton = False
    app.onStatsButton = False
    generateWorkSessions(app)
    generateWeeklyEvents(app)
    getShownTimes(app)

### Code from https://www.freecodecamp.org/news/how-to-create-a-csv-file-in-python/ ###

def importHabitData():
    habits = set()
    with open("habitData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            habits.add(Habit(row[0], row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')))
    return habits

def importSingleEventData():
    singleEvents = set()
    with open("singleEventData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            color = row[4].replace('|', ',')
            singleEvents.add(SingleEvent(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[2], '%Y-%m-%d').date(), row[3], color))
    return singleEvents

def importSplitEventData():
    splitEvents = set()
    with open("splitEventData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            color = row[5].replace('|', ',')
            splitEvents.add(SplitEvent(row[0], int(row[1]), int(row[2]), datetime.strptime(row[3], '%Y-%m-%d').date(), row[4], color))
    return splitEvents

def writeHabitData(name, days, startTime, endTime):
    with open('habitData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, days, startTime, endTime])

def writeSingleEventData(startTime, endTime, date, name, fill):
    with open('singleEventData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([startTime, endTime, date, name, fill])

def writeSplitEventData(deadline, durationMinutes, durationHours, date, name, fill):
    with open('splitEventData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([deadline, durationMinutes, durationHours, date, name, fill])

#######################################################################################

def redrawAll(app):
    drawTaskBar(app)
    if app.calendar == True:
        date = app.currentDate + timedelta(days=app.timeDelta)
        drawCalendar(app, app.currentDate, getDatesList(date))
        if app.taskPopUp:
            drawTaskPopUp(app.taskName)
            drawCheckBox(app.singleEventChecked)
            if app.singleEventChecked:
                drawSingleEventMenu(app.startTime, app.endTime, app.currentDate, app.clickedDayButton, app.rect1Fill, app.rect2Fill)
            else:
                drawMultipleEventsMenu(app.deadline, app.durationHours, app.durationMinutes, app.currentDate, app.clickedDayButton, app.deadlineFill, app.plusOpacity, app.minusOpacity)
    elif app.tasks == True:
        drawTasks(app)
    elif app.habits == True:
        drawHabits(app)
        if app.habitsPopUp:
            drawHabitsPopUp(app.habitName, app.habitStartTime, app.habitEndTime, app.selectedHabitDays, app.rect3Fill, app.rect4Fill)
    elif app.stats == True:
        drawStats(app)

def drawTaskBar(app):
    drawRect(0, 0, 78, 78, fill=rgb(25, 28, 28))
    logo = Image.open('Images/hourglasslogo.png') # Icon taken from https://www.facebook.com/subtleclassics/
    drawRect(0, 78, 78, 702, fill=rgb(25, 28, 28))
    drawImage(CMUImage(logo), 39, 39, align='center', width=35, height=35)
    calendar = Image.open('Images/calendar.png') # Icon taken from https://www.flaticon.com/free-icon/calendar_3239948?term=calendar&page=1&position=13&origin=search&related_id=3239948
    drawRect(0, 78, 78, 78, fill=rgb(36, 42, 47), opacity = app.calendarButtonOpacity)
    drawImage(CMUImage(calendar), 39, 117, align='center', width=23, height=23)
    tasks = Image.open('Images/tasks.png') # Icon taken from https://www.flaticon.com/free-icon/clipboard_839860?term=clipboard&page=1&position=2&origin=search&related_id=839860
    drawRect(0, 156, 78, 78, fill=rgb(36, 42, 47), opacity = app.tasksButtonOpacity)
    drawImage(CMUImage(tasks), 39, 195, align='center', width=23, height=23)
    habits = Image.open('Images/habits.png') # Icon taken from https://www.flaticon.com/free-icon/refresh_10899351?term=habits&page=1&position=29&origin=search&related_id=10899351
    drawRect(0, 234, 78, 78, fill=rgb(36, 42, 47), opacity = app.habitsButtonOpacity)
    drawImage(CMUImage(habits), 39, 273, align='center', width=23, height=23)
    stats = Image.open('Images/graph.png') # Icon taken from https://www.flaticon.com/free-icon/graph_2567943?term=stats&page=1&position=3&origin=tag&related_id=2567943
    drawRect(0, 312, 78, 78, fill=rgb(36, 42, 47), opacity = app.statsButtonOpacity)
    drawImage(CMUImage(stats), 39, 351, align='center', width=23, height=23)

def onMouseMove(app, mouseX, mouseY):
    checkOnButton(app, mouseX, mouseY)

def checkOnButton(app, mouseX, mouseY):
    if 0 <= mouseX <= 78:
        if 78 < mouseY < 156:
            app.onCalendarButton = True
        else:
            app.onCalendarButton = False
        if 156 < mouseY < 234:
            app.onTasksButton = True
        else:
            app.onTasksButton = False
        if 234 < mouseY < 312:
            app.onHabitsButton = True
        else:
            app.onHabitsButton = False
        if 312 < mouseY < 390:
            app.onStatsButton = True
        else:
            app.onStatsButton = False
    else:
        app.onCalendarButton = False
        app.onTasksButton = False
        app.onHabitsButton = False
        app.onStatsButton = False
    if app.taskPopUp and app.singleEventChecked:
        if 810 <= mouseX <= 940 and 135 <= mouseY <= 175 and app.rect1Fill != rgb(255, 204, 203):
                app.rect1Fill = rgb(238, 241, 247)
        elif app.rect1Fill != rgb(255, 204, 203):
            app.rect1Fill = rgb(255, 255, 255)
        if 980 <= mouseX <= 1115 and 135 <= mouseY <= 175 and app.rect2Fill != rgb(255, 204, 203):
                app.rect2Fill = rgb(238, 241, 247)
        elif app.rect2Fill != rgb(255, 204, 203):
            app.rect2Fill = rgb(255, 255, 255)
    elif app.taskPopUp:
        if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
            app.deadlineFill = rgb(238, 241, 247)
        else:
            app.deadlineFill = rgb(255, 255, 255)
        if 926 <= mouseX <= 950 and 130 <= mouseY <= 154:
            app.minusOpacity = 100
        else:
            app.minusOpacity = 0
        if 1053 <= mouseX <= 1073 and 132 <= mouseY <= 152:
            app.plusOpacity = 100
        else:
            app.plusOpacity = 0
    elif app.habitsPopUp:
        if 806 <= mouseX <= 936 and 121 <= mouseY <= 161:
            app.rect3Fill = rgb(238, 241, 247)
        else:
            app.rect3Fill = rgb(255, 255, 255)
        if 975 <= mouseX <= 1105 and 121 <= mouseY <= 161:
            app.rect4Fill = rgb(238, 241, 247)
        else:
            app.rect4Fill = rgb(255, 255, 255)

def onStep(app):
    modifyButtonOpacity(app)
    checkInTextField(app)
    checkTextFieldLegality(app)
    checkDeadlineLegality(app)

def modifyButtonOpacity(app):
    if app.onCalendarButton and app.calendarButtonOpacity < 100:
        app.calendarButtonOpacity += 25
    elif app.onTasksButton and app.tasksButtonOpacity < 100:
        app.tasksButtonOpacity += 25
    elif app.onHabitsButton and app.habitsButtonOpacity < 100:
        app.habitsButtonOpacity += 25
    elif app.onStatsButton and app.statsButtonOpacity < 100:
        app.statsButtonOpacity += 25
    if app.calendarButtonOpacity != 0 and app.onCalendarButton == False:
        app.calendarButtonOpacity -= 25
    if app.tasksButtonOpacity != 0 and app.onTasksButton == False:
        app.tasksButtonOpacity -= 25
    if app.habitsButtonOpacity != 0 and app.onHabitsButton == False:
        app.habitsButtonOpacity -= 25
    if app.statsButtonOpacity != 0 and app.onStatsButton == False:
        app.statsButtonOpacity -= 25

def onMousePress(app, mouseX, mouseY):
    checkButtonPress(app, mouseX, mouseY)
    if app.taskPopUp and app.singleEventChecked:
        checkDayButtonPresses(mouseX, mouseY, app.singleEventDayButtonList)
        checkStartEndTimePresses(app, mouseX, mouseY)
    elif app.taskPopUp:
        checkDeadlinePress(app, mouseX, mouseY)
        checkDurationPress(app, mouseX, mouseY)
        checkPlusMinusButtons(app, mouseX, mouseY)
        checkDayButtonPresses(mouseX, mouseY, app.splitEventDayButtonList)
    elif app.habitsPopUp:
        checkHabitStartEndTimePresses(app, mouseX, mouseY)
        checkMultiDayButtonPresses(app, mouseX, mouseY, [(810, 211), (905, 211), (1000, 211), (1095, 211), (810, 266), (905, 266), (1000, 266), (1095, 266)])

def checkPlusMinusButtons(app, mouseX, mouseY):
    if 926 <= mouseX <= 950 and 130 <= mouseY <= 154:
        if app.durationMinutes == 0:
            app.durationHours -= 1
            app.durationMinutes = 45
        elif app.durationHours == 0 and app.durationMinutes == 15:
            return
        else:
            app.durationMinutes -= 15
    if 1053 <= mouseX <= 1073 and 132 <= mouseY <= 152:
        if app.durationMinutes + 15 != 60:
            app.durationMinutes += 15
        else:
            app.durationHours += 1
            app.durationMinutes = 0

def checkButtonPress(app, mouseX, mouseY):
    if 0 <= mouseX <= 78:
        if 78 < mouseY < 156:
            app.calendar = True
            app.tasks = False
            app.habits = False
            app.stats = False
        elif 156 < mouseY < 234:
            app.tasks = True
            app.calendar = False
            app.habits = False
            app.stats = False
        elif 234 < mouseY < 312:
            app.tasks = False
            app.habits = True
            app.calendar = False
            app.stats = False
        elif 312 < mouseY < 390:
            app.tasks = False
            app.habits = False
            app.calendar = False
            app.stats = True
    elif 1224 < mouseX < 1352 and app.calendar == True:
        if 13 <= mouseY <= 65:
            app.taskPopUp = True
    elif 1224 < mouseX < 1352 and app.habits == True:
        if 13 <= mouseY <= 65:
            app.habitsPopUp = True
    if app.taskPopUp and app.singleEventChecked:
        if 810 <= mouseX <= 1190:
            if 32 <= mouseY <= 60:
                app.cursorTimer = 8
                app.taskNameTextField = True
            else:
                app.taskNameTextField = False
                app.taskName = app.taskName.replace('|', '')
        else:
            app.taskNameTextField = False
            app.taskName = app.taskName.replace('|', '')
        if 1095 < mouseX < 1193:
            if 344 < mouseY < 384:
                if app.selectedDate != None and app.rect1Fill != rgb(255, 204, 203) and app.rect2Fill != rgb(255, 204, 203) and 'Task name' not in app.taskName and isLegalTime(app):
                    app.startTime = app.startTime.replace('|', '')
                    app.endTime = app.endTime.replace('|', '')
                    fill = app.colorPalette[random.randrange(10)]
                    app.singleEventTasks.add(SingleEvent(datetime.strptime(app.startTime, '%I:%M%p'), datetime.strptime(app.endTime, '%I:%M%p'), app.selectedDate, app.taskName, fill))
                    writeSingleEventData(datetime.strptime(app.startTime, '%I:%M%p'), datetime.strptime(app.endTime, '%I:%M%p'), app.selectedDate, app.taskName, fill)
                    app.selectedDate = None
                    app.rect1Fill = rgb(255, 255, 255)
                    app.rect2Fill = rgb(255, 255, 255)
                    app.taskName = 'Task name'
                    app.taskNameTextField = False
                    app.cursorTimer = 8
                    app.clickedDayButton = 9
                    app.startTime = '12:00pm'
                    app.endTime = '12:00am'
                    app.taskPopUp = False
                    generateWeeklyEvents(app)
                    generateWorkSessions(app)
                elif app.rect1Fill != rgb(255, 204, 203) and app.rect2Fill != rgb(255, 204, 203) and isLegalTime(app) == False:
                    app.rect1Fill = rgb(255, 204, 203)
                    app.rect2Fill = rgb(255, 204, 203)
        if 1022 <= mouseX <= 1078:
            if 354 <= mouseY <= 374:
                app.taskPopUp = False
                app.taskName = 'Task name'
                app.taskNameTextField = False
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.startTime = '12:00pm'
                app.endTime = '12:00am'
        if 810 <= mouseX <= 830:
            if 95 <= mouseY <= 115:
                app.singleEventChecked = not app.singleEventChecked
                app.selectedDate = None
    elif app.taskPopUp:
        if 810 <= mouseX <= 1190:
            if 32 <= mouseY <= 60:
                app.cursorTimer = 8
                app.taskNameTextField = True
            else:
                app.taskNameTextField = False
                app.taskName = app.taskName.replace('|', '')
        else:
            app.taskNameTextField = False
            app.taskName = app.taskName.replace('|', '')
        if 1095 < mouseX < 1193: # Schedule Button
            if 344 < mouseY < 384:
                if app.selectedDate != None and app.deadlineFill != rgb(255, 204, 203) and 'Task name' not in app.taskName and isLegalDeadline(app):
                    fill = app.colorPalette[random.randrange(10)]
                    app.splitTasks.add(SplitEvent(app.deadline, app.durationMinutes, app.durationHours, app.selectedDate, app.taskName, fill))
                    writeSplitEventData(app.deadline, app.durationMinutes, app.durationHours, app.selectedDate, app.taskName, fill)
                    app.durationMinutes = 15
                    app.durationHours = 0
                    app.deadline = app.deadline.replace('|', '')
                    app.selectedDate = None
                    app.deadlineFill = rgb(255, 255, 255)
                    app.taskName = 'Task name'
                    app.cursorTimer = 8
                    app.clickedDayButton = 9
                    app.taskNameTextField = False
                    app.taskPopUp = False
                    generateWeeklyEvents(app)
                    generateWorkSessions(app)
        if 1022 <= mouseX <= 1078: # Cancel button
            if 354 <= mouseY <= 374:
                app.taskName = 'Task name'
                app.deadline = '12:00pm'
                app.taskNameTextField = False
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.durationMinutes = 15
                app.durationHours = 0
                app.taskPopUp = False
        if 810 <= mouseX <= 830:
            if 95 <= mouseY <= 115:
                app.singleEventChecked = not app.singleEventChecked
        if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
            app.cursorTimer = 8
            app.deadlineTextField = True
        else:
            app.deadlineTextField = False
            app.deadline = app.deadline.replace('|', '')
    if app.habitsPopUp:
        if 1022 <= mouseX <= 1078: # Cancel button
            if 354 <= mouseY <= 374:
                app.habitsPopUp = False
        if 1095 < mouseX < 1193: # Schedule Button
            if 344 < mouseY < 384:
                if app.selectedHabitDays != set() and app.rect3Fill != rgb(255, 204, 203) and app.rect4Fill != rgb(255, 204, 203) and 'Habit name' not in app.habitName and isLegalHabitTime(app):
                    app.habitStartTime = app.habitStartTime.replace('|', '')
                    app.habitEndTime = app.habitEndTime.replace('|', '')
                    app.habitsSet.add(Habit(app.habitName, app.selectedHabitDays, datetime.strptime(app.habitStartTime, '%I:%M%p'), datetime.strptime(app.habitEndTime, '%I:%M%p')))
                    writeHabitData(app.habitName, app.selectedHabitDays, datetime.strptime(app.habitStartTime, '%I:%M%p'), datetime.strptime(app.habitEndTime, '%I:%M%p'))
                    app.habitName = 'Habit name'
                    app.selectedHabitDays = set()
                    app.rect3Fill = rgb(255, 255, 255)
                    app.rect4Fill = rgb(255, 255, 255)
                    app.habitsPopUp = False
                    generateWeeklyEvents(app)
                    generateWorkSessions(app)
                elif app.rect3Fill != rgb(255, 204, 203) and app.rect4Fill != rgb(255, 204, 203) and isLegalHabitTime(app) == False:
                    app.rect3Fill = rgb(255, 204, 203)
                    app.rect4Fill = rgb(255, 204, 203)
        if 810 <= mouseX <= 1190 and 32 <= mouseY <= 60:
            app.cursorTimer = 8
            app.habitsNameTextField = True
        else:
            app.habitsNameTextField = False
            app.habitName = app.habitName.replace('|', '')

def onKeyPress(app, key):
    if app.taskPopUp == False:
        if key == 'right':
            app.timeDelta += 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWeeklyEvents(app)
            generateWorkSessions(app)
        elif key == 'left':
            app.timeDelta -= 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWeeklyEvents(app)
            generateWorkSessions(app)
        elif key == 'up' and app.index > 0:
            app.index -= 1
            getShownTimes(app)
        elif key == 'down' and app.index < 16:
            app.index += 1
            getShownTimes(app)
    elif app.taskNameTextField:
        app.cursorTimer = 0
        app.taskName = app.taskName.replace('|', '')
        app.taskName += '|'
        if app.taskName == 'Task nam|' or app.taskName == 'Task name|':
            app.taskName = '|'
        if key == 'space' and len(app.taskName) < 21:
            app.taskName = app.taskName[:-1] + ' ' + '|'
        elif key == 'backspace':
            app.taskName = app.taskName[:-2] + '|'
        elif len(app.taskName) < 18:
            app.taskName = app.taskName[:-1] + key + '|'
    if app.habitsNameTextField:
        app.cursorTimer = 0
        app.habitName = app.habitName.replace('|', '')
        app.habitName += '|'
        if app.habitName == 'Habit nam|' or app.habitName == 'Habit name|':
            app.habitName = '|'
        if key == 'space' and len(app.habitName) < 21:
            app.habitName = app.habitName[:-1] + ' ' + '|'
        elif key == 'backspace':
            app.habitName = app.habitName[:-2] + '|'
        elif len(app.habitName) < 18:
            app.habitName = app.habitName[:-1] + key + '|'
    if app.rect1TextField:
        app.cursorTimer = 0
        app.startTime = app.startTime.replace('|', '')
        app.startTime += '|'
        if key == 'backspace':
            app.startTime = app.startTime[:-2] + '|'
        elif len(app.startTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.startTime = app.startTime[:-1] + key + '|'
    if app.rect2TextField:
        app.cursorTimer = 0
        app.endTime = app.endTime.replace('|', '')
        app.endTime += '|'
        if key == 'backspace':
            app.endTime = app.endTime[:-2] + '|'
        elif len(app.endTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.endTime = app.endTime[:-1] + key + '|'
    if app.rect3TextField:
        app.cursorTimer = 0
        app.habitStartTime = app.habitStartTime.replace('|', '')
        app.habitStartTime += '|'
        if key == 'backspace':
            app.habitStartTime = app.habitStartTime[:-2] + '|'
        elif len(app.habitStartTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitStartTime = app.habitStartTime[:-1] + key + '|'
    if app.rect4TextField:
        app.cursorTimer = 0
        app.habitEndTime = app.habitEndTime.replace('|', '')
        app.habitEndTime += '|'
        if key == 'backspace':
            app.habitEndTime = app.habitEndTime[:-2] + '|'
        elif len(app.habitEndTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitEndTime = app.habitEndTime[:-1] + key + '|'
    if app.deadlineTextField:
        app.cursorTimer = 0
        app.deadline = app.deadline.replace('|', '')
        app.deadline += '|'
        if key == 'backspace':
            app.deadline = app.deadline[:-2] + '|'
        elif len(app.deadline) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.deadline = app.deadline[:-1] + key + '|'

runApp(width = 1366, height = 780)