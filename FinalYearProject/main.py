from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from firebase import firebase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.graphics import Line
from kivy.clock import Clock
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
    correctAnswers = 0
    incorrectAnswers = 0


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
        answer = int(answer)

        if answer == self.expectedAnswer:
            print("correct answer")
        else:
            print("incorrect answer")

        globalVariables.roundNumber += 1

        self.reinitialize()

    def reinitialize(self):
        if globalVariables.roundNumber > 10:
            # end the minigame
            pass
        else:
            algo.algo(globalVariables.operation, globalVariables.level)
            self.updateText()

class LoginPage(Screen):
    # gets the username and password if the person has logged in before
    try:
        ScreenManagement.store.get('credentials')['username']
    except KeyError:
        username = ""
    else:
        username = ScreenManagement.store.get('credentials')['username']
    try:
        ScreenManagement.store.get('credentials')['password']
    except KeyError:
        password = ""
    else:
        password = ScreenManagement.store.get('credentials')['password']

    def checkLogin(self, uname, pword):
        if self.loginLoop(uname, pword) == -1:
            print('this username and password do not match anything in the database')
        else:
            ScreenManagement.store.put('credentials', username=uname, password=pword,
                                       email=ScreenManagement.store.get('credentials')['email'],
                                       teacher=ScreenManagement.store.get('credentials')['teacher'],
                                       classroom=ScreenManagement.store.get('credentials')['classroom'])
            self.manager.current = 'main'

    def loginLoop(self, uname, pword):
        while True:
            results = firebase.get('/users/', None)

            for index in results:
                if results[index]['username'] == uname and results[index]['password'] == pword:
                    return 1

            return -1


class RegisterPage(Screen):
    def checkPassword(self, uname, email, pword):
        capital = any(x.isupper() for x in pword)
        lowercase = any(x.islower() for x in pword)
        number = any(x.isnumeric() for x in pword)
        length = len(pword)

        if length < 8 or number is False or lowercase is False or capital is False:
            print(
                'Make sure that your password is at least 8 characters long and contains 1 uppercase letter and 1 number')
        else:
            self.checkRegister(uname, email, pword)

    def checkRegister(self, uname, email, pword):
        if self.registerLoop(uname, email) == -1:
            print('data not added to the DB')
        else:
            firebase.post('/users',
                          {'username': uname, 'email': email, 'password': pword, 'teacher': 'no',
                           'classroom': "no classroom"})
            ScreenManagement.store.put('credentials', username=uname, password=pword, email=email, teacher="no",
                                       classroom="no classroom")
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
    classroom = "no classroom"

    try:
        ScreenManagement.store.get('credentials')['classroom']
    except KeyError:
        classroom = "no classroom"

    def deleteClassroom(self):
        # replace classroom in JSON store with 0
        # replace classroom in DB with 0
        pass

    def joinClassroom(self):
        # check the DB to see if the classroom name exists
        # if it exists, add the classroom name to the students DB and to the JSON store of the device
        # if it doesn't exist then write to the screen to check if the classroom definitely exists
        pass


class TeacherClassroomPage(Screen):
    pass


class PlayPage(Screen):
    pass


class AdditionPage(Screen):
    playerXP = 600

    def playGame(self, levelNumber):
        # algo.algo("add", levelNumber)

        globalVariables.level = levelNumber
        globalVariables.operation = "add"

        self.manager.current = 'minigame'


class SubtractionPage(Screen):
    playerXP = 600

    def playGame(self, levelNumber):
        # algo.algo("subtract", levelNumber)
        globalVariables.level = levelNumber
        globalVariables.operation = "subtract"

        self.manager.current = 'minigame'


class MultiplicationPage(Screen):
    playerXP = 600

    def playGame(self, levelNumber):
        # algo.algo("multiply", levelNumber)
        globalVariables.level = levelNumber
        globalVariables.operation = "multiply"

        self.manager.current = 'minigame'


class DivisionPage(Screen):
    playerXP = 600

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
