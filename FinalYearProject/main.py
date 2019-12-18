from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from firebase import firebase
from kivy.core.window import Window

firebase = firebase.FirebaseApplication('https://c16324311fyp.firebaseio.com/')

# https://www.youtube.com/watch?v=Q3HdZMtBQUw
# post gives garbage string as parent and then multiple pieces of data go afterwards
# firebase.post('/users', {'nameOfFirstData': 'actualDataValue', 'nameOfSecondData': 'actualDataValue'})
# firebase.post('/users', {'username': 'testymctestface', 'email': 'test@test.test', 'password': '12345'})


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
        print("joining classroom...")

    # should be pop up
    # if user doesnt have a classroom already
    # ask what the classroom ID is
    # check if the classroom ID exists
    # if it exists then allow user to join the classroom
    def createClassroom(self):
        print("creating classroom...")
# should be a pop up
        # if the user doesn't already has a classroom then allow to create one.
        # assign unique classroom ID to classroom


class PlayPage(Screen):
    pass


kv_file = Builder.load_file('fyp.kv')


class FYPApp(App):
    def builder(self):
        return kv_file


if __name__ == '__main__':
    FYPApp().run()
