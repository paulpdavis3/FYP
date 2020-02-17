from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from firebase import firebase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

firebase = firebase.FirebaseApplication('https://c16324311fyp.firebaseio.com/')


# https://www.youtube.com/watch?v=Q3HdZMtBQUw
# post gives garbage string as parent and then multiple pieces of data go afterwards
# firebase.post('/users', {'nameOfFirstData': 'actualDataValue', 'nameOfSecondData': 'actualDataValue'})
# firebase.post('/users', {'username': 'testymctestface', 'email': 'test@test.test', 'password': '12345'})

class JoinClassroomPopup(FloatLayout):
    def joinClassroomButton(self):
        print("button pressed")


class CreateClassroomPopup(FloatLayout):
    def createClassroomButton(self):
        # 1. should only be for teachers
        # 2. if they are already the teacher of a classroom then they can create more
        print("button pressed")


def showJoinPopup(hasClassroom):
    show = JoinClassroomPopup()
    if hasClassroom == "yes":
        print("hello")
    else:
        print("hello but no classroom")
    popupWindow = Popup(title="Join Classroom", content=show, size_hint=(None, None), size=(400, 400))

    popupWindow.open()


def showCreatePopup():
    show = CreateClassroomPopup()
    popupWindow = Popup(title="Create Classroom", content=show, size_hint=(None, None), size=(400, 400))

    popupWindow.open()


class ScreenManagement(ScreenManager):
    pass


class TitlePage(Screen):
    # Window.clearcolor = (0.5, 0.1, 0.1, 0.1)  # Sets the colour of the background. Tuple is in the format (R, G, B, S) S for saturation.
    pass


class LoginPage(Screen):
    def checkLogin(self, uname, pword):
        if self.loginLoop(uname, pword) == -1:
            print('this username and password do not match anything in the database')
        else:
            print('log in successful')
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
            firebase.post('/users', {'username': uname, 'email': email, 'password': pword})
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
    pass


class ProgressPage(Screen):
    pass


class ProfilePage(Screen):
    pass


class ClassroomPage(Screen):

    def joinClassroom(self):
        # if they are already part of a classroom then show the name and offer to delete it
        # if they aren't part of a classroom allow them to input the classroom code and verify it exists, then join the classroom

        # there should already be a global variable that contains the users info so we will know if they have a classroom or not
        results = firebase.get('/users/', None)
        print(results)
        classroomName = 0
        if classroomName != 0:
            showJoinPopup("yes")
        else:
            showJoinPopup("no")

    def createClassroom(self):
        showCreatePopup()

class PlayPage(Screen):
    pass


kv_file = Builder.load_file('fyp.kv')


class FYPApp(App):
    def builder(self):
        return kv_file


if __name__ == '__main__':
    FYPApp().run()
