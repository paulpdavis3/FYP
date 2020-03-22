from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
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
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
import algo
import time
import random
import globalVariables

firebase = firebase.FirebaseApplication('https://c16324311fyp.firebaseio.com/')


# Create a new db for just classrooms to avoid checking all users to save time

# https://www.youtube.com/watch?v=Q3HdZMtBQUw
# post gives garbage string as parent and then multiple pieces of data go afterwards
# firebase.post('/users', {'nameOfFirstData': 'actualDataValue', 'nameOfSecondData': 'actualDataValue'})
# firebase.post('/users', {'username': 'testymctestface', 'email': 'test@test.test', 'password': '12345', 'teacher': 'yes', 'classroom': 'test'})


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

    def on_enter(self, *args):
        globalVariables.correctAnswers = 0
        globalVariables.incorrectAnswers = 0
        globalVariables.roundNumber = 1
        self.reinitialize()

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
            self.potentialAnswer2 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer3 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer4 = str(self.expectedAnswer + random.randrange(-5, 5))
        elif randomNum == 1:
            self.potentialAnswer1 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer2 = str(self.expectedAnswer)
            self.potentialAnswer3 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer4 = str(self.expectedAnswer + random.randrange(-5, 5))
        elif randomNum == 2:
            self.potentialAnswer1 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer2 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer3 = str(self.expectedAnswer)
            self.potentialAnswer4 = str(self.expectedAnswer + random.randrange(-5, 5))
        elif randomNum == 3:
            self.potentialAnswer1 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer2 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer3 = str(self.expectedAnswer + random.randrange(-5, 5))
            self.potentialAnswer4 = str(self.expectedAnswer)

    def checkAnswer(self, answer):
        answer = float(answer)

        if answer == self.expectedAnswer:
            print("correct answer")
            globalVariables.correctAnswers += 1
        else:
            print("incorrect answer")
            globalVariables.incorrectAnswers += 1

        globalVariables.roundNumber += 1

        self.reinitialize()

    def reinitialize(self):
        if globalVariables.roundNumber > 10:
            self.manager.current = 'results'
        else:
            algo.algo(globalVariables.operation, globalVariables.level)
            self.updateText()


class ResultsPage(Screen):
    correctAnswers = StringProperty()
    incorrectAnswers = StringProperty()
    xpEarned = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.progressValue = 0

    def on_enter(self, *args):
        self.progressValue = Clock.create_trigger(self.updateBar)
        self.correctAnswers = str(globalVariables.correctAnswers)
        xpEarned = self.correctAnswers * 10  # * timerMultiplier which will be a multiplier if the user finishes under 30 seconds, if over 1 minute to answer all maybe 0.75 multiplier


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
        else:
            # ScreenManagement.store.put('credentials', username=uname, password=pword,
            #                            email=ScreenManagement.store.get('credentials')['email'],
            #                            teacher=ScreenManagement.store.get('credentials')['teacher'],
            #                            classroom=ScreenManagement.store.get('credentials')['classroom'])
            self.manager.current = 'main'

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
        else:
            self.checkRegister(uname, email, pword, isTeacher)

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
                    print("this username is already taken")
                    return -1
                elif results[index]['email'] == email:
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


class ProgressPage(Screen):
    pass


class ProfilePage(Screen):
    pass


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
            self.ids.studentClassroomName.text = self.classroom
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
            self.ids.teacherClassroomName.text = self.classroom
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


kv_file = Builder.load_file('fyp.kv')


class FYPApp(App):
    def builder(self):
        return kv_file


if __name__ == '__main__':
    globalVariables.initialize()
    FYPApp().run()
