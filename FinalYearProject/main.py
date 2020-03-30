from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, partial
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from firebase import firebase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Line
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
import algo
import popups
import time
import random
import globalVariables
import math
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
import re

LabelBase.register(name="Helvetica",
                   fn_regular="Fonts/HelveticaTextbookLTRoman.ttf")

firebase = firebase.FirebaseApplication('https://c16324311fyp.firebaseio.com/')


# Create a new db for just classrooms to avoid checking all users to save time

# https://www.youtube.com/watch?v=Q3HdZMtBQUw
# post gives garbage string as parent and then multiple pieces of data go afterwards
# firebase.post('/users', {'nameOfFirstData': 'actualDataValue', 'nameOfSecondData': 'actualDataValue'})
# firebase.post('/users',{'username': 'uname', 'email': 'email', 'password': 'pword', 'teacher': "yes",'classroom': "teachersclassroom", 'add': 0, 'subtract': 0, 'multiply': 0, 'divide': 0})


class ScreenManagement(ScreenManager):
    data_dir = App().user_data_dir
    store = JsonStore(join(data_dir, 'storage.json'))


class TitlePage(Screen):
    Window.clearcolor = (1, 72 / 255, 72 / 255,
                         1)  # Sets the colour of the background. Tuple is in the format (R, G, B, S) S for saturation.
    pass


class MinigamePage(Screen):
    xNum = StringProperty()
    yNum = StringProperty()
    zNum = StringProperty()
    answer = StringProperty()
    levelNum = StringProperty()
    roundNum = StringProperty()
    operator = StringProperty()
    potentialAnswer1 = StringProperty()
    potentialAnswer2 = StringProperty()
    potentialAnswer3 = StringProperty()
    potentialAnswer4 = StringProperty()
    expectedAnswer = 0
    timer = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.xNum = str(0)
        self.yNum = str(0)
        self.zNum = str(0)
        self.answer = str(0)
        self.levelNum = str(0)
        self.roundNum = str(0)
        self.operator = str(0)
        self.expectedAnswer = 0
        self.correctSound = SoundLoader.load("Sounds/correct.wav")
        self.incorrectSound = SoundLoader.load("Sounds/incorrect.wav")

        self.timer = "00:00"

    def on_enter(self, *args):
        globalVariables.correctAnswers = 0
        globalVariables.incorrectAnswers = 0
        globalVariables.roundNumber = 1
        globalVariables.seconds = 0
        globalVariables.minutes = 0
        self.reinitialize()
        Clock.schedule_interval(self.incrementTimer, .1)
        self.incrementTimer(0)
        self.startTimer()

    def incrementTimer(self, interval):
        if int(globalVariables.seconds) == 59:
            globalVariables.seconds = 0
            globalVariables.minutes += 1

        if globalVariables.seconds > 9:
            self.timer = "0" + str(globalVariables.minutes) + ":" + str(round(globalVariables.seconds))
        else:
            self.timer = "0" + str(globalVariables.minutes) + ":0" + str(round(globalVariables.seconds))

        globalVariables.seconds += .1

    def startTimer(self):
        Clock.unschedule(self.incrementTimer)
        Clock.schedule_interval(self.incrementTimer, .1)

    def stopTimer(self):
        Clock.unschedule(self.incrementTimer)

    def updateText(self):
        if globalVariables.blank == 0:
            self.xNum = str("?")
            self.expectedAnswer = globalVariables.x
        else:
            self.xNum = str(globalVariables.x)
        if globalVariables.blank == 1:
            self.yNum = str("?")
            self.expectedAnswer = globalVariables.y
        else:
            self.yNum = str(globalVariables.y)
        if globalVariables.blank == 2:
            self.answer = str("?")
            self.expectedAnswer = globalVariables.answer
        else:
            self.answer = str(globalVariables.answer)

        self.levelNum = str(globalVariables.level)
        self.roundNum = str(globalVariables.roundNumber)
        if globalVariables.operation == "add":
            self.operator = str("+")
        elif globalVariables.operation == "subtract":
            self.operator = str("-")
        if globalVariables.operation == "multiply":
            self.operator = str("x")
        elif globalVariables.operation == "divide":
            self.operator = str("÷")

        randomNum = random.randrange(0, 4)

        if randomNum == 0:
            self.potentialAnswer1 = str(self.expectedAnswer)
            self.potentialAnswer2 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer3 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer4 = str(self.getPotentialAnswer(self.expectedAnswer))
        elif randomNum == 1:
            self.potentialAnswer1 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer2 = str(self.expectedAnswer)
            self.potentialAnswer3 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer4 = str(self.getPotentialAnswer(self.expectedAnswer))
        elif randomNum == 2:
            self.potentialAnswer1 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer2 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer3 = str(self.expectedAnswer)
            self.potentialAnswer4 = str(self.getPotentialAnswer(self.expectedAnswer))
        elif randomNum == 3:
            self.potentialAnswer1 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer2 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer3 = str(self.getPotentialAnswer(self.expectedAnswer))
            self.potentialAnswer4 = str(self.expectedAnswer)

    def getPotentialAnswer(self, expectedAnswer):
        expectedAnswerLength = len(str(expectedAnswer))
        potentialAnswer = expectedAnswer
        potentialAnswerCheck = 0

        difficultyMapped = int((((globalVariables.level - 1) * (1 - 9)) / (10 - 1)) + 9)

        if expectedAnswerLength == 1:
            while potentialAnswerCheck == 0:
                potentialAnswer = expectedAnswer + random.randrange(-difficultyMapped, difficultyMapped)
                if potentialAnswer != expectedAnswer and potentialAnswer > 0:
                    potentialAnswerCheck = 1
        elif expectedAnswerLength == 2:
            expectedAnswerSingles = expectedAnswer % 10
            expectedAnswerTens = int(str(expectedAnswer % 100)[0])
            while potentialAnswerCheck == 0:
                potentialAnswer = int(str(expectedAnswerTens + random.randrange(-difficultyMapped, difficultyMapped)) + str(
                    expectedAnswerSingles))
                if potentialAnswer != expectedAnswer and potentialAnswer >= 0:
                    potentialAnswerCheck = 1
        elif expectedAnswerLength == 3:
            expectedAnswerSingles = expectedAnswer % 10
            expectedAnswerTens = int(str(expectedAnswer % 100)[0])
            expectedAnswerHundreds = str(expectedAnswer)[0]
            while potentialAnswerCheck == 0:
                potentialAnswer = int(
                    str(int(expectedAnswerHundreds) + random.randrange(-difficultyMapped, difficultyMapped)) + str(
                        expectedAnswerTens) + str(expectedAnswerSingles))
                if potentialAnswer != expectedAnswer and 0 <= potentialAnswer < 1000:
                    potentialAnswerCheck = 1

        return potentialAnswer

    def checkAnswer(self, answer):
        answer = float(answer)

        if answer == self.expectedAnswer:
            self.correctSound.play()
            print("correct answer")
            globalVariables.correctAnswers += 1
        else:
            self.incorrectSound.play()
            print("incorrect answer")
            globalVariables.incorrectAnswers += 1

        globalVariables.roundNumber += 1

        self.reinitialize()

    def reinitialize(self):
        if globalVariables.roundNumber > 10:
            self.stopTimer()
            self.manager.current = 'results'
        else:
            algo.algo(globalVariables.operation, globalVariables.level)
            self.updateText()

    def goBack(self):
        popups.LeaveMinigamePopup()


class ResultsPage(Screen):
    xpEarned = 0

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.ids.resultsInfo.text = "You got \n" + str(globalVariables.correctAnswers) + " out of 10 \nquestions correct"
        xpEarned = ((int(globalVariables.correctAnswers) * 5) * (
                30 / ((globalVariables.minutes * 60) + globalVariables.seconds))) - (
                       int(globalVariables.incorrectAnswers * 10))

        if xpEarned < int(globalVariables.correctAnswers):
            xpEarned = int(globalVariables.correctAnswers)

        currentXP = ScreenManagement.store.get('credentials')[globalVariables.operation]

        currentXP += xpEarned

        if currentXP > 1000:
            currentXP = 1000

        if globalVariables.operation == "add":
            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'],
                                       add=currentXP,
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            if self.updateUserDatabase("add", currentXP) == 1:
                print("update db successfully")
            else:
                print("couldnt update db")
        elif globalVariables.operation == "subtract":
            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'],
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=currentXP,
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            if self.updateUserDatabase("add", currentXP) == 1:
                print("update db successfully")
            else:
                print("couldnt update db")
        elif globalVariables.operation == "multiply":
            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'],
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=currentXP,
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            if self.updateUserDatabase("add", currentXP) == 1:
                print("update db successfully")
            else:
                print("couldnt update db")
        elif globalVariables.operation == "divide":
            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'],
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=currentXP)
            if self.updateUserDatabase("add", currentXP) == 1:
                print("update db successfully")
            else:
                print("couldnt update db")

        nextHundred = int(math.ceil(currentXP / 100.0)) * 100
        print(currentXP, nextHundred)
        self.ids.progressBar.value = (int(currentXP) / int(nextHundred)) * 100

        if globalVariables.operation == "add":
            self.ids.resultsOverallXP.text = "Overall XP for Addition: " + str(int(currentXP))
        elif globalVariables.operation == "subtract":
            self.ids.resultsOverallXP.text = "Overall XP for Subtraction: " + str(int(currentXP))
        elif globalVariables.operation == "multiply":
            self.ids.resultsOverallXP.text = "Overall XP for Multiplication: " + str(int(currentXP))
        elif globalVariables.operation == "divide":
            self.ids.resultsOverallXP.text = "Overall XP for Division: " + str(int(currentXP))
        self.ids.resultsNextLevel.text = str(int(nextHundred - currentXP)) + "xp until next level"

    def updateUserDatabase(self, operator, xp):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, operator, xp)
                    return 1

            return -1


class LoginPage(Screen):
    # gets the username and password if the person has logged in before
    username = StringProperty()
    password = StringProperty()

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['username']
        except KeyError:
            self.username = ""
        else:
            self.username = ScreenManagement.store.get('credentials')['username']
        try:
            ScreenManagement.store.get('credentials')['password']
        except KeyError:
            self.password = ""
        else:
            self.password = ScreenManagement.store.get('credentials')['password']

    def checkLogin(self, uname, pword):
        if self.loginLoop(uname, pword) == -1:
            print('this username and password do not match anything in the database')
            return popups.UsernameAndPasswordPopup()
        else:
            if self.updateJsonLoop(uname) == 1:
                print("successfully updated JSON file")
            else:
                print("couldn't update JSON file")

            self.manager.current = 'main'

    def updateJsonLoop(self, username):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == username:
                    ScreenManagement.store.put('credentials',
                                               username=results[index]['username'],
                                               password=results[index]['password'],
                                               email=results[index]['email'],
                                               teacher=results[index]['teacher'],
                                               classroom=results[index]['classroom'],
                                               add=results[index]['add'],
                                               subtract=results[index]['subtract'],
                                               multiply=results[index]['multiply'],
                                               divide=results[index]['divide'])
                    return 1

            return -1

    def loginLoop(self, uname, pword):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == uname and results[index]['password'] == pword:
                    return 1

            return -1


class RegisterPage(Screen):
    def checkPassword(self, uname, email, pword, isTeacher):
        capital = any(x.isupper() for x in pword)
        lowercase = any(x.islower() for x in pword)
        number = any(x.isnumeric() for x in pword)
        length = len(pword)

        if length < 8 or number is False or lowercase is False or capital is False:
            print(
                'Make sure that your password is at least 8 characters long and contains 1 uppercase letter and 1 number')
            return popups.PasswordPopup()

        elif re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            self.checkRegister(uname, email, pword, isTeacher)
        else:
            print("invalid email")
            return popups.InvalidEmailPopup()

    def checkRegister(self, uname, email, pword, isTeacher):
        if self.registerLoop(uname, email) == -1:
            print('data not added to the DB')
        else:
            if isTeacher:
                firebase.post('/users',
                              {'username': uname, 'email': email, 'password': pword, 'teacher': "yes",
                               'classroom': "no classroom", 'add': 0, 'subtract': 0, 'multiply': 0, 'divide': 0})
                ScreenManagement.store.put('credentials', username=uname, password=pword, email=email, teacher="yes",
                                           classroom="no classroom", add=0, subtract=0, multiply=0, divide=0)
                print('data added to the db successfully')
                self.manager.current = 'login'
            else:
                firebase.post('/users',
                              {'username': uname, 'email': email, 'password': pword, 'teacher': "no",
                               'classroom': "no classroom", 'add': 0, 'subtract': 0, 'multiply': 0, 'divide': 0})
                ScreenManagement.store.put('credentials', username=uname, password=pword, email=email, teacher="no",
                                           classroom="no classroom", add=0, subtract=0, multiply=0, divide=0)
                print('data added to the db successfully')
                self.manager.current = 'login'

    def registerLoop(self, uname, email):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == uname:
                    popups.UsernamePopup()
                    print("this username is already taken")
                    return -1
                elif results[index]['email'] == email:
                    popups.EmailPopup()
                    print("this email is already taken")
                    return -1

            return 1


class MainPage(Screen):
    def goToClassroom(self):
        if ScreenManagement.store.get('credentials')['teacher'] == "no":
            # go to join classroom
            self.manager.current = "studentclassroom"
        else:
            # go to create classroom
            self.manager.current = "teacherclassroom"

    def goToProgress(self):
        if ScreenManagement.store.get('credentials')['teacher'] == "no":
            # go to join classroom
            self.manager.current = "studentprogress"
        else:
            # go to create classroom
            self.manager.current = "teacherprogress"

    def goToProfile(self):
        if ScreenManagement.store.get('credentials')['teacher'] == "no":
            # go to join classroom
            self.manager.current = "studentprofile"
        else:
            # go to create classroom
            self.manager.current = "teacherprofile"

    def logOut(self):
        return popups.LogOutPopup()


class StudentProgressPage(Screen):
    pass


class TeacherProgressPage(Screen):
    view = ObjectProperty(None)

    check = 0

    def on_pre_enter(self, *args):
        self.createScrollview(1)

    def createScrollview(self, dt):

        studentList = []

        results = firebase.get('/users/', None)

        for index in results:
            if results[index]['classroom'] == ScreenManagement.store.get('credentials')['classroom'] and results[index][
                'username'] != ScreenManagement.store.get('credentials')['username']:
                studentList.append(results[index]['username'])

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        for studentName in studentList:
            layout.add_widget(Button(on_release=partial(self.studentInfo, studentName),
                                     text=studentName, font_size=self.width*0.08,
                                     size_hint=(0.8, None),
                                     font_name='Helvetica',
                                     background_normal="button.png",
                                     background_down="buttondown.png",
                                     color=(1, 72 / 255, 72 / 255, 1)))
        scrollview = ScrollView(id="scrollview", size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

    def studentInfo(self, *args):
        globalVariables.studentName = args[0]
        self.manager.current = 'studentinfo'

    def on_leave(self, *args):
        print(self.view.children[0])
        self.view.remove_widget(self.view.children[0])


class StudentInfoPage(Screen):

    def on_pre_enter(self, *args):
        if self.findStudent() == 1:
            print("student found")
        else:
            print("Unable to find student")

    def findStudent(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == globalVariables.studentName:
                    self.ids.studentInfoTitle.text = globalVariables.studentName
                    self.ids.addition.text = "Total Addition XP: " + str(int(results[index]['add']))
                    self.ids.subtraction.text = "Total Subtraction XP: " + str(int(results[index]['subtract']))
                    self.ids.multiplication.text = "Total Multiplication XP: " + str(int(results[index]['multiply']))
                    self.ids.division.text = "Total Division XP: " + str(int(results[index]['divide']))
                    self.ids.overall.text = "Overall XP: " + str(
                        int(results[index]['divide']) + (results[index]['multiply']) + (
                            results[index]['subtract']) + int(results[index]['add']))
                    return 1

            return -1

    def goBack(self):
        self.manager.current = "teacherprogress"

    def removeFromClassroom(self, studentName):
        results = firebase.get('/users/', None)

        for index in results:
            if results[index]['username'] == globalVariables.studentName:
                firebase.put('/users/' + index, 'classroom', 'no classroom')
                self.manager.current = "teacherprogress"


class AdditionProgressPage(Screen):
    def on_enter(self, *args):
        self.reinitialize()

    def reinitialize(self):
        self.ids.studentAdditionInfo.text = "Total Addition XP: " + str(
            int(ScreenManagement.store.get('credentials')['add']))

    def resetAddition(self):
        ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                   password=ScreenManagement.store.get('credentials')['password'],
                                   email=ScreenManagement.store.get('credentials')['email'],
                                   teacher=ScreenManagement.store.get('credentials')['teacher'],
                                   classroom=ScreenManagement.store.get('credentials'['classroom']),
                                   add=0,
                                   subtract=ScreenManagement.store.get('credentials')['subtract'],
                                   multiply=ScreenManagement.store.get('credentials')['multiply'],
                                   divide=ScreenManagement.store.get('credentials')['divide'])

        self.resetAdditionDB()
        self.reinitialize()

    def resetAdditionDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'add', 0)
                    return 1
            return -1


class SubtractionProgressPage(Screen):
    def on_enter(self, *args):
        self.reinitialize()

    def reinitialize(self):
        self.ids.studentSubtractionInfo.text = "Total Subtraction XP: " + str(
            int(ScreenManagement.store.get('credentials')['subtract']))

    def resetSubtraction(self):
        ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                   password=ScreenManagement.store.get('credentials')['password'],
                                   email=ScreenManagement.store.get('credentials')['email'],
                                   teacher=ScreenManagement.store.get('credentials')['teacher'],
                                   classroom=ScreenManagement.store.get('credentials'['classroom']),
                                   add=ScreenManagement.store.get('credentials')['add'],
                                   subtract=0,
                                   multiply=ScreenManagement.store.get('credentials')['multiply'],
                                   divide=ScreenManagement.store.get('credentials')['divide'])

        self.resetSubtractionDB()
        self.reinitialize()

    def resetSubtractionDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'subtract', 0)
                    return 1
            return -1


class MultiplicationProgressPage(Screen):
    def on_enter(self, *args):
        self.reinitialize()

    def reinitialize(self):
        self.ids.studentMultiplicationInfo.text = "Total Multiplication XP: " + str(
            int(ScreenManagement.store.get('credentials')['multiply']))

    def resetMultiplication(self):
        ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                   password=ScreenManagement.store.get('credentials')['password'],
                                   email=ScreenManagement.store.get('credentials')['email'],
                                   teacher=ScreenManagement.store.get('credentials')['teacher'],
                                   classroom=ScreenManagement.store.get('credentials'['classroom']),
                                   add=ScreenManagement.store.get('credentials')['add'],
                                   subtract=ScreenManagement.store.get('credentials')['subtract'],
                                   multiply=0,
                                   divide=ScreenManagement.store.get('credentials')['divide'])

        self.resetMultiplicationDB()
        self.reinitialize()

    def resetMultiplicationDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'multiply', 0)
                    return 1
            return -1


class DivisionProgressPage(Screen):
    def on_enter(self, *args):
        self.reinitialize()

    def reinitialize(self):
        self.ids.studentDivisionInfo.text = "Total Division XP: " + str(
            int(ScreenManagement.store.get('credentials')['divide']))

    def resetDivision(self):
        ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                   password=ScreenManagement.store.get('credentials')['password'],
                                   email=ScreenManagement.store.get('credentials')['email'],
                                   teacher=ScreenManagement.store.get('credentials')['teacher'],
                                   classroom=ScreenManagement.store.get('credentials'['classroom']),
                                   add=ScreenManagement.store.get('credentials')['add'],
                                   subtract=ScreenManagement.store.get('credentials')['subtract'],
                                   multiply=ScreenManagement.store.get('credentials')['multiply'],
                                   divide=0)

        self.resetDivisionDB()
        self.reinitialize()

    def resetDivisionDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'divide', 0)
                    return 1
            return -1


class StudentProfilePage(Screen):

    def on_pre_enter(self, *args):
        print("student profile page")
        self.updateText()

    def updateText(self):
        self.ids.username.text = ScreenManagement.store.get('credentials')['username'] + "'s Profile"

    def changeUsername(self, new):

        old = ScreenManagement.store.get('credentials')['username']

        self.changeUsernameLoop(old, new)

        ScreenManagement.store.put('credentials', username=new,
                                   password=ScreenManagement.store.get('credentials')['password'],
                                   email=ScreenManagement.store.get('credentials')['email'],
                                   teacher=ScreenManagement.store.get('credentials')['teacher'],
                                   classroom=ScreenManagement.store.get('credentials')['classroom'],
                                   add=ScreenManagement.store.get('credentials')['add'],
                                   subtract=ScreenManagement.store.get('credentials')['subtract'],
                                   multiply=ScreenManagement.store.get('credentials')['multiply'],
                                   divide=ScreenManagement.store.get('credentials')['divide'])
        self.updateText()

    def changeUsernameLoop(self, oldUsername, newUsername):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == oldUsername:
                    firebase.put('/users/' + index, 'username', newUsername)
                    return 1
            return -1

    def deleteUser(self):
        if self.deleteUserDB() == 1:
            ScreenManagement.store.put('credentials', username="",
                                       password="",
                                       email="",
                                       teacher="",
                                       classroom="",
                                       add="",
                                       subtract="",
                                       multiply="",
                                       divide="")
            self.manager.current = "login"
            print("successfully deleted user")
        else:
            print("couldn't delete user from db")

    def deleteUserDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.delete('/users/', index)
                    return 1
            return -1


class TeacherProfilePage(Screen):
    def on_pre_enter(self, *args):
        print("teacher profile page")
        self.updateText()

    def updateText(self):
        self.ids.username.text = ScreenManagement.store.get('credentials')['username'] + "'s Profile"

    def changeUsername(self, new):

        old = ScreenManagement.store.get('credentials')['username']

        if self.changeUsernameLoop(new) == 1:
            ScreenManagement.store.put('credentials', username=new,
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'],
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            print("successfully changed username")
            self.updateText()
        else:
            print("unable to change username")

    def changeUsernameLoop(self, newUsername):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'username', newUsername)
                    return 1
            return -1

    def deleteUser(self):
        if self.deleteUserDB() == 1:
            ScreenManagement.store.put('credentials', username="",
                                       password="",
                                       email="",
                                       teacher="",
                                       classroom="",
                                       add="",
                                       subtract="",
                                       multiply="",
                                       divide="")
            self.manager.current = "login"
            print("successfully deleted user")
        else:
            print("couldn't delete user from db")

    def deleteUserDB(self):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.delete('/users/', index)
                    return 1
            return -1


class StudentClassroomPage(Screen):
    classroom = ""

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['classroom']
        except KeyError:
            self.classroom = "no classroom"
        else:
            self.classroom = ScreenManagement.store.get('credentials')['classroom']

        self.updatePage()

    def updatePage(self):
        self.classroom = ScreenManagement.store.get('credentials')['classroom']
        if self.classroom == "no classroom":
            self.ids.studentClassroomName.text = "No Classroom"
            self.ids.studentLeaveClassroom.disabled = True
            self.ids.studentJoinClassroom.disabled = False
            self.ids.studentClassroomJoin.text = "Enter the name of the classroom you'd like to join"
        else:
            self.ids.studentClassroomName.text = "Current Classroom: " + self.classroom
            self.ids.studentLeaveClassroom.disabled = False
            self.ids.studentJoinClassroom.disabled = True
            self.ids.studentClassroomJoin.text = "Press the button below to leave your current classroom"

    def leaveClassroom(self, classroomName):
        if self.checkClassroomLoop(classroomName) == -1:
            print("Classroom doesn't exist")
        else:
            if self.leaveUserClassroomLoop(classroomName) == -1:
                print("Unable to leave classroom from users data in database")
            else:
                print("Successfully left classroom from users info in db")

            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom="no classroom",
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            print("Classroom Successfully Left")
            self.updatePage()

    def leaveUserClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'classroom', "no classroom")
                    return 1

            return -1

    def joinClassroom(self, classroomName):
        if self.checkClassroomLoop(classroomName) == -1:
            print("classroom doesn't exist")
        else:
            if self.joinUserClassroomLoop(classroomName) == -1:
                print("Unable to join classroom in database")
            else:
                print("Successfully joined classroom in db")

            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=classroomName,
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            print("joined classroom successfully")
            self.updatePage()

    def checkClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/classrooms/', None)

            for index in results:
                if results[index]['classroomName'] == classroomName:
                    return 1

            return -1

    def joinUserClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'classroom', classroomName)
                    return 1

            return -1


class TeacherClassroomPage(Screen):
    classroom = "no classroom"

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['classroom']
        except KeyError:
            self.classroom = "no classroom"
        else:
            self.classroom = ScreenManagement.store.get('credentials')['classroom']

        self.updatePage()

    def updatePage(self):
        self.classroom = ScreenManagement.store.get('credentials')['classroom']
        if self.classroom == "no classroom":
            self.ids.teacherClassroomName.text = "No Classroom"
            self.ids.teacherDeleteClassroom.disabled = True
            self.ids.teacherCreateClassroom.disabled = False
            self.ids.teacherClassroomCreate.text = "Enter the name of your classroom below"
        else:
            self.ids.teacherClassroomName.text = "Your Classroom: " + self.classroom
            self.ids.teacherDeleteClassroom.disabled = False
            self.ids.teacherCreateClassroom.disabled = True
            self.ids.teacherClassroomCreate.text = "Press the button below to delete your current classroom"

    def createClassroom(self, classroomName):

        if self.createClassroomLoop(classroomName) == -1:
            print("classroom already exists")
        else:
            firebase.post('/classrooms',
                          {'classroomName': classroomName})

            if self.createUserClassroomLoop(classroomName) == -1:
                print("Unable to add classroom to users data in database")
            else:
                print("Successfully added classroom to users info in db")

            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=classroomName,
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            print("created classroom successfully")
            self.updatePage()

    def createClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/classrooms/', None)

            for index in results:
                if results[index]['classroomName'] == classroomName:
                    return -1

            return 1

    def createUserClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'classroom', classroomName)
                    return 1

            return -1

    def deleteClassroom(self, classroomName):

        if self.deleteClassroomLoop(classroomName) == -1:
            print("Unable to delete this classroom / Classroom doesn't exist")
        else:

            if self.deleteUserClassroomLoop(classroomName) == -1:
                print("Unable to remove classroom from users data in database")
            else:
                print("Successfully removed classroom from users info in db")

            ScreenManagement.store.put('credentials', username=ScreenManagement.store.get('credentials')['username'],
                                       password=ScreenManagement.store.get('credentials')['password'],
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom="no classroom",
                                       add=ScreenManagement.store.get('credentials')['add'],
                                       subtract=ScreenManagement.store.get('credentials')['subtract'],
                                       multiply=ScreenManagement.store.get('credentials')['multiply'],
                                       divide=ScreenManagement.store.get('credentials')['divide'])
            print("Classroom Successfully Deleted")
            self.updatePage()

    def deleteClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/classrooms/', None)

            for index in results:
                if results[index]['classroomName'] == classroomName:
                    firebase.delete('/classrooms', index)
                    return 1

            return -1

    def deleteUserClassroomLoop(self, classroomName):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == ScreenManagement.store.get('credentials')['username']:
                    firebase.put('/users/' + index, 'classroom', "no classroom")
                    return 1

            return -1


class PlayPage(Screen):
    pass


class AdditionPage(Screen):
    playerXP = 0

    # if something breaks there was a block of code here that said:
    # addButton1 = ObjectProperty() ...

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['add']
        except KeyError:
            self.playerXP = 0
        else:
            self.playerXP = int(ScreenManagement.store.get('credentials')['add'])

        self.disabledButtons()

    def disabledButtons(self):
        if self.playerXP < 100:
            self.ids.addButton2.disabled = True
        if self.playerXP < 200:
            self.ids.addButton3.disabled = True
        if self.playerXP < 300:
            self.ids.addButton4.disabled = True
        if self.playerXP < 400:
            self.ids.addButton5.disabled = True
        if self.playerXP < 500:
            self.ids.addButton6.disabled = True
        if self.playerXP < 600:
            self.ids.addButton7.disabled = True
        if self.playerXP < 700:
            self.ids.addButton8.disabled = True
        if self.playerXP < 800:
            self.ids.addButton9.disabled = True
        if self.playerXP < 900:
            self.ids.addButton10.disabled = True

    def playGame(self, levelNumber):
        # algo.algo("add", levelNumber)

        globalVariables.level = levelNumber
        globalVariables.operation = "add"

        self.manager.current = 'minigame'


class SubtractionPage(Screen):
    playerXP = 0

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['subtract']
        except KeyError:
            self.playerXP = 0
        else:
            self.playerXP = int(ScreenManagement.store.get('credentials')['subtract'])

        self.disabledButtons()

    def disabledButtons(self):
        if self.playerXP < 100:
            self.ids.subtractButton2.disabled = True
        if self.playerXP < 200:
            self.ids.subtractButton3.disabled = True
        if self.playerXP < 300:
            self.ids.subtractButton4.disabled = True
        if self.playerXP < 400:
            self.ids.subtractButton5.disabled = True
        if self.playerXP < 500:
            self.ids.subtractButton6.disabled = True
        if self.playerXP < 600:
            self.ids.subtractButton7.disabled = True
        if self.playerXP < 700:
            self.ids.subtractButton8.disabled = True
        if self.playerXP < 800:
            self.ids.subtractButton9.disabled = True
        if self.playerXP < 900:
            self.ids.subtractButton10.disabled = True

    def playGame(self, levelNumber):
        # algo.algo("subtract", levelNumber)
        globalVariables.level = levelNumber
        globalVariables.operation = "subtract"

        self.manager.current = 'minigame'


class MultiplicationPage(Screen):
    playerXP = 0

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['multiply']
        except KeyError:
            self.playerXP = 0
        else:
            self.playerXP = int(ScreenManagement.store.get('credentials')['multiply'])

        self.disabledButtons()

    def disabledButtons(self):
        if self.playerXP < 100:
            self.ids.multiplyButton2.disabled = True
        if self.playerXP < 200:
            self.ids.multiplyButton3.disabled = True
        if self.playerXP < 300:
            self.ids.multiplyButton4.disabled = True
        if self.playerXP < 400:
            self.ids.multiplyButton5.disabled = True
        if self.playerXP < 500:
            self.ids.multiplyButton6.disabled = True
        if self.playerXP < 600:
            self.ids.multiplyButton7.disabled = True
        if self.playerXP < 700:
            self.ids.multiplyButton8.disabled = True
        if self.playerXP < 800:
            self.ids.multiplyButton9.disabled = True
        if self.playerXP < 900:
            self.ids.multiplyButton10.disabled = True

    def playGame(self, levelNumber):
        # algo.algo("multiply", levelNumber)
        globalVariables.level = levelNumber
        globalVariables.operation = "multiply"

        self.manager.current = 'minigame'


class DivisionPage(Screen):
    playerXP = 0

    def on_pre_enter(self, *args):
        try:
            ScreenManagement.store.get('credentials')['divide']
        except KeyError:
            self.playerXP = 0
        else:
            self.playerXP = int(ScreenManagement.store.get('credentials')['divide'])

        self.disabledButtons()

    def disabledButtons(self):
        if self.playerXP < 100:
            self.ids.divideButton2.disabled = True
        if self.playerXP < 200:
            self.ids.divideButton3.disabled = True
        if self.playerXP < 300:
            self.ids.divideButton4.disabled = True
        if self.playerXP < 400:
            self.ids.divideButton5.disabled = True
        if self.playerXP < 500:
            self.ids.divideButton6.disabled = True
        if self.playerXP < 600:
            self.ids.divideButton7.disabled = True
        if self.playerXP < 700:
            self.ids.divideButton8.disabled = True
        if self.playerXP < 800:
            self.ids.divideButton9.disabled = True
        if self.playerXP < 900:
            self.ids.divideButton10.disabled = True

    def playGame(self, levelNumber):
        # algo.algo("divide", levelNumber)
        globalVariables.level = levelNumber
        globalVariables.operation = "divide"

        self.manager.current = 'minigame'


# kv_file = Builder.load_file('fyp.kv')


class FYPApp(App):
    def builder(self, kv_file=None):
        return kv_file


if __name__ == '__main__':
    globalVariables.initialize()
    FYPApp().run()
