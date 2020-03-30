from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class LogOutDialog(Popup):
    pass


class LogOutPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(LogOutPopup, self).__init__(**kwargs)
        self.dialog = LogOutDialog()
        self.dialog.open()


class UsernameAndPasswordDialog(Popup):
    pass


class UsernameAndPasswordPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(UsernameAndPasswordPopup, self).__init__(**kwargs)
        self.dialog = UsernameAndPasswordDialog()
        self.dialog.open()


class PasswordDialog(Popup):
    pass


class PasswordPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(PasswordPopup, self).__init__(**kwargs)
        self.dialog = PasswordDialog()
        self.dialog.open()


class EmailDialog(Popup):
    pass


class EmailPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(EmailPopup, self).__init__(**kwargs)
        self.dialog = EmailDialog()
        self.dialog.open()


class InvalidEmailDialog(Popup):
    pass


class InvalidEmailPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(InvalidEmailPopup, self).__init__(**kwargs)
        self.dialog = InvalidEmailDialog()
        self.dialog.open()


class UsernameDialog(Popup):
    pass


class UsernamePopup(BoxLayout):
    def __init__(self, **kwargs):
        super(UsernamePopup, self).__init__(**kwargs)
        self.dialog = UsernameDialog()
        self.dialog.open()

class LeaveMinigameDialog(Popup):
    pass


class LeaveMinigamePopup(BoxLayout):
    def __init__(self, **kwargs):
        super(LeaveMinigamePopup, self).__init__(**kwargs)
        self.dialog = LeaveMinigameDialog()
        self.dialog.open()