from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.config import Config


Window.clearcolor = (1, 1, 1, 1)
Window.size = (1000, 10000)
Builder.load_file('app.kv')


#Score is a universal variable
score = 0

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        #Overall Layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        # Welcome Text
        layout.add_widget(Label(text="Productivity Score Calculator", font_size=60, size_hint=(1, 0.1)))

        #Preperation Time Input
        prep_time_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=40, center_x = 250)

        # Prep time label
        prep_time_layout.add_widget(Label(text="Preparation Time(Rounded\nto the nearest minute):", font_size=60, size_hint=(0.5, 0.17)))

        #Prep time input
        self.prep_time_real_input = TextInput(hint_text="30", size_hint=(0.033, 0.085), multiline=False, font_size = "60")
        prep_time_layout.add_widget(self.prep_time_real_input)



        layout.add_widget(prep_time_layout)
        self.add_widget(layout)

    def switch_to_screen(self, screen_name):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen_name



class MyApp(App):
    def build(self):
        self.title = "Productivity Score Calculator"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))


        return sm


if __name__ == '__main__':
    MyApp().run()
