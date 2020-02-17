from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from firebase import firebase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from os.path import join

firebase = firebase.FirebaseApplication('https://c16324311fyp.firebaseio.com/')

# https://www.youtube.com/watch?v=Q3HdZMtBQUw
# post gives garbage string as parent and then multiple pieces of data go afterwards
# firebase.post('/users', {'nameOfFirstData': 'actualDataValue', 'nameOfSecondData': 'actualDataValue'})
firebase.post('/users',
              {'username': 'testymctestface', 'email': 'test@test.test', 'password': '12345', 'teacher': 'yes',
               'classroom': 'test'})


class JoinClassroomPopup(FloatLayout):
    joinClassroomPopupText = ''

    def joinClassroomButton(self):
        print("button pressed")

    def deleteClassroomButton(self):
        print("button pressed")


class CreateClassroomPopup(FloatLayout):
    createClassroomPopupText = ''

    def createClassroomButton(self):
        print("button pressed")


def showJoinPopup(classroomName):
    # changes text of the popup depending on whether the user belongs to a classroom or not
    if classroomName != "no":
        JoinClassroomPopup.joinClassroomPopupText = "has classroom: " + classroomName
    else:
        JoinClassroomPopup.joinClassroomPopupText = "has no classroom"

    show = JoinClassroomPopup()

    popupWindow = Popup(title="Join Classroom", content=show, size_hint=(0.7, 0.7))

    popupWindow.open()


def showCreatePopup(isTeacher):
    # changes text of the popup depending on whether the user is a teacher or not
    if isTeacher == "yes":
        CreateClassroomPopup.createClassroomPopupText = "this person is a teacher"
    elif isTeacher == "no":
        CreateClassroomPopup.createClassroomPopupText = "this person is not a teacher"
    show = CreateClassroomPopup()
    popupWindow = Popup(title="Create Classroom", content=show, size_hint=(0.7, 0.7))

    popupWindow.open()


class ScreenManagement(ScreenManager):
    data_dir = App().user_data_dir
    store = JsonStore(join(data_dir, 'storage.json'))


class TitlePage(Screen):
    # Window.clearcolor = (0.5, 0.1, 0.1, 0.1)  # Sets the colour of the background. Tuple is in the format (R, G, B, S) S for saturation.
    pass


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
            ScreenManagement.store.put('credentials', username=uname, password=pword)
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
            ScreenManagement.store.put('credentials', username=uname, password=pword, email=email, teacher="no",
                                       classroom=0)
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
        try:
            ScreenManagement.store.get('credentials')['classroom']
        except KeyError:
            classroomName = 0
        else:
            classroomName = ScreenManagement.store.get('credentials')['classroom']

        if classroomName != 0:
            showJoinPopup(classroomName)
        else:
            showJoinPopup("no")

    def createClassroom(self):
        # 1. should only be for teachers
        # 2. if they are already the teacher of a classroom then they can create more

        try:
            ScreenManagement.store.get('credentials')['teacher']
        except KeyError:
            isTeacher = "no"
        else:
            isTeacher = ScreenManagement.store.get('credentials')['teacher']

        showCreatePopup(isTeacher)


class PlayPage(Screen):
    pass


kv_file = Builder.load_file('fyp.kv')


class FYPApp(App):
    def builder(self):
        return kv_file


if __name__ == '__main__':
    FYPApp().run()
