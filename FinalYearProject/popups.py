from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class LogOutDialog(Popup):
    pass


class LogOutPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(LogOutPopup, self).__init__(**kwargs)
        self.dialog = LogOutDialog()
        self.dialog.open()
