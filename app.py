from tkinter import Widget

from PIL.ImageChops import overlay
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
from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


Window.clearcolor = (1, 1, 1, 1)
Window.size = (1000, 10000)
Builder.load_file('app.kv')


#Score is a universal variable
score = 0


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        #Overall Layout
        layout = RelativeLayout()



        # Welcome Text
        welcome_layout = RelativeLayout(size_hint=(1, 0.1), pos_hint={"center_x":0.5, "center_y":0.9})
        welcome_label = Label(text="Productivity Score Calculator", font_size=75, size_hint=(1, 0.1), pos_hint={"center_x":0.5, "center_y":0.9})
        with welcome_label.canvas:
            Color("deeppink")
            Rectangle(pos=welcome_label.pos, size=welcome_label.size)
        welcome_layout.add_widget(welcome_label)




        #Preparation Time Input Layout
        prep_time_layout = RelativeLayout(size_hint=(1, 0.2), pos_hint={"center_x":0.5, "center_y":0.75})

        # Prep time label
        prep_time_layout.add_widget(Label(text="Preparation Time(Rounded to the nearest minute):", font_size=60, size_hint=(0.5, 0.17), pos_hint={"x":0.1, "center_y":0.75}))

        #Prep time input
        self.prep_time_real_input = TextInput(hint_text="30", size_hint=(0.06, 0.27), multiline=False, font_size = "60", pos_hint={"center_x":0.95, "center_y":0.75}, input_filter="int")
        prep_time_layout.add_widget(self.prep_time_real_input)


        # Minor Errors Input Layout
        minor_errors_layout = RelativeLayout(size_hint=(1, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.65})

        # Minor Errors label
        minor_errors_layout.add_widget(
            Label(text="Number of minor errors:", font_size=60, size_hint=(0.5, 0.17),
                  pos_hint={"x": 0.1, "center_y": 0.65}))

        # Minor Errors input
        self.minor_errors_real_input = TextInput(hint_text="5", size_hint=(0.06, 0.27), multiline=False, font_size="60",
                                              pos_hint={"center_x": 0.95, "center_y": 0.65}, input_filter="int")
        minor_errors_layout.add_widget(self.minor_errors_real_input)


        # Medium Errors Input Layout
        medium_errors_layout = RelativeLayout(size_hint=(1, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.55})

        # Medium Errors label
        medium_errors_layout.add_widget(
            Label(text="Number of medium level errors:", font_size=60, size_hint=(0.5, 0.17),
                  pos_hint={"x": 0.1, "center_y": 0.55}))

        # Medium Errors input
        self.medium_errors_real_input = TextInput(hint_text="3", size_hint=(0.06, 0.27), multiline=False, font_size="60",
                                                 pos_hint={"center_x": 0.95, "center_y": 0.55}, input_filter="int")
        medium_errors_layout.add_widget(self.medium_errors_real_input)

        # Severe Errors Input Layout
        severe_errors_layout = RelativeLayout(size_hint=(1, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.45})

        # Severe Errors label
        severe_errors_layout.add_widget(
            Label(text="Number of severe level errors:", font_size=60, size_hint=(0.5, 0.17),
                  pos_hint={"x": 0.1, "center_y": 0.45}))

        # Severe Errors input
        self.severe_errors_real_input = TextInput(hint_text="1", size_hint=(0.06, 0.27), multiline=False,
                                                  font_size="60",
                                                  pos_hint={"center_x": 0.95, "center_y": 0.45}, input_filter="int")
        severe_errors_layout.add_widget(self.severe_errors_real_input)

        # Calculate Button
        calculate_btn = Button(text="Calculate", size_hint=(0.5, 0.1), background_color="deeppink",
                           color=(1, 1, 1, 1), background_normal='', pos_hint={"center_x": 0.5, "center_y": 0.3}, font_size="60")
        calculate_btn.bind(on_press=self.calculate)

        # About Button
        about_btn = Button(text="About This", size_hint=(0.5, 0.1), background_color="deeppink",
                               color=(1, 1, 1, 1), background_normal='', pos_hint={"center_x": 0.5, "center_y": 0.15},
                               font_size="60")
        about_btn.bind(on_press=self.go_to_about)


        layout.add_widget(welcome_layout)
        layout.add_widget(prep_time_layout)
        layout.add_widget(minor_errors_layout)
        layout.add_widget(medium_errors_layout)
        layout.add_widget(severe_errors_layout)
        layout.add_widget(calculate_btn)
        layout.add_widget(about_btn)
        self.add_widget(layout)

    def switch_to_screen(self, screen_name):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen_name

    def calculate(self, instance):
        global score#This will be changed
        #Collect all of the inputs and store them as variables
        try:
            prep_time = int(self.prep_time_real_input.text)
            minor_errors_count = int(self.minor_errors_real_input.text)
            medium_errors_count = int(self.medium_errors_real_input.text)
            severe_errors_count = int(self.severe_errors_real_input.text)

            #Ensure that all of the variables are not negative, if not, make them positive
            if prep_time < 0:
                prep_time *= -1

            if minor_errors_count < 0:
                minor_errors_count *= -1

            if medium_errors_count < 0:
                medium_errors_count *= -1

            if severe_errors_count < 0:
                severe_errors_count *= -1

            #Perform the calculation!!!

            #Score is 100 by default
            temp_score = 100

            temp_score -= minor_errors_count*3#Subtract 3 for every minor error

            temp_score -= medium_errors_count*10#Subtract 10 for every medium error

            temp_score -= severe_errors_count*40#Subtract 40 for every severe error

            time_penalty = 0#Time penalty variable is established

            #Based of the time taken to prepare it, change the penalty
            if prep_time < 25:
                time_penalty = 0#Make sure time penalty is 0
            elif 25<=prep_time<=35:
                time_penalty = 3
            elif 35<prep_time<=45:
                time_penalty = 6
            elif 45<prep_time<=60:
                time_penalty = 12
            else:#Time is over an hour
                time_penalty = 25

            temp_score -= time_penalty#Subtract the time penalty from the score

            score = temp_score#set the score!!!

        except:
            print("problem")

            #Make a POPUP ERROR!!!!:)
            #Make a temp layout
            layout = GridLayout(cols=1, padding=10)

            #Make a label for that layout and a button also
            popupLabel = Label(text="Error Processing Your Request, Please Ensure That All\n Fields Have Been Filled With Natural Numbers", font_size = "60", color=(1,1,1,1))
            closeButton = Button(text="Exit Back To Home Screen",
                                     background_color="deeppink", color=(1, 1, 1, 1),
                                     background_normal='', font_size = "60")

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            popup = Popup(title='An Error Occurred',
                              content=layout, separator_color="deeppink", overlay_color="deeppink", title_color = (1,1,1,1))#Make the popup
            popup.open()#Open the popup

            closeButton.bind(on_press=popup.dismiss)#Make the button close the window

        else:#If no exception occurred and the data is ready

            # Make a POPUP to display the results!!!!!!!:)
            # Make a temp layout
            layout = GridLayout(cols=1, padding=10)

            # Make a label for that layout and a button also
            popupLabel = Label(
                text=f"Based off a prep time of {prep_time} minute(s), {minor_errors_count} minor error(s),\n {medium_errors_count} medium-level error(s), and {severe_errors_count} severe error(s),\n a score of {score} was calculated.", font_size = "60", color=(1,1,1,1))
            closeButton = Button(text="Exit Back To Home Screen",
                                 background_color="deeppink", color=(1, 1, 1, 1),
                                 background_normal='', font_size = "60")

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            popup = Popup(title='Your Results',
                          content=layout, separator_color="deeppink", overlay_color="deeppink", title_color = (1,1,1,1))  # Make the popup
            popup.open()  # Open the popup

            closeButton.bind(on_press=popup.dismiss)  # Make the button close the window

    def go_to_about(self, instance):
        self.switch_to_screen("about")

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

        # Overall Layout
        layout = RelativeLayout()

        #Add the title text
        layout.add_widget(Label(text="About This:", font_size=75, size_hint=(1, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.95}, bold=True))

        #Add the body text pieces
        layout.add_widget(Label(text="This was a project made for Pendo which will help them measure how \nproductive an AI is at making basic standard contracts.", font_size=60, size_hint=(1, 0.1), pos_hint={"x": 0.01, "center_y": 0.85}))
        layout.add_widget(Label(text="This app takes in the time made to prepare a standard contract,\n the number of minor errors, the number of medium-level errors,\n and the number of severe errors in order to make a productivity score.", font_size=60, size_hint=(1, 0.1), pos_hint={"x": 0.01, "center_y": 0.7}))
        layout.add_widget(Label(text="The penalty for prep time in minutes m is as follows:\n| 0<=m<25: 0 | 25<=m<=35: -3 | 35<m<=45: -6 | 45<m<=60: -12 |\n| m>60: -25 |", font_size=60, size_hint=(1, 0.1), pos_hint={"x": -0.035, "center_y": 0.53}))
        layout.add_widget(Label(text="The formula for the score is: \n100 - timepenalty - (3 x numberofminorerrors)\n - (10 x numberofmediumlevelerrors) - (40 x number of severe errors)", font_size=60, size_hint=(1, 0.1), pos_hint={"x": 0.01, "center_y": 0.35}))
        layout.add_widget(Label(text="The github link for this is \nhttps://github.com/atulbhai1/TimeAndAccuracyScoreCalculatorPen\ndoforOrby#", font_size=60, size_hint=(1, 0.1), pos_hint={"x": 0.01, "center_y": 0.17}))


        self.add_widget(layout)

class MyApp(App):
    def build(self):
        self.title = "Productivity Score Calculator"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AboutScreen(name="about"))


        return sm


if __name__ == '__main__':
    MyApp().run()



