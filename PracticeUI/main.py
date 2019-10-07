import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.Joystick import Joystick
from kivy.uix.image import Image, AsyncImage
from kivy.animation import Animation
from kivy.core.window import Window
import threading
import time

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN_NAME = 'NewScreen'
GAME_SCREEN_NAME = 'game'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    on = False
    counter = 0

    def __init__(self, **kwargs):
        Window.clearcolor = (0, 0, 0, 1)
        super(MainScreen, self).__init__(**kwargs)

    def transition(self):
        SCREEN_MANAGER.current = NEW_SCREEN_NAME

    def to_game_screen(self):
        SCREEN_MANAGER.current = GAME_SCREEN_NAME

    def pressed2(self):
        self.counter += 1
        return "%s" % self.counter

    def pressed3(self):
        return str(self.counter)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        self.on = not self.on

        return self.on

        # PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

class Game(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('Game.kv')
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        if not self._keyboard:
            return
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def to_main_screen(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def thread_function2(self):
        y = threading.Thread(target=self.move_iron_man(), daemon=True)
        y.start()

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.ids.hero.x -= 50
        elif keycode[1] == 'right':
            self.ids.hero.x += 50
        elif keycode[1] == 'up':
            self.ids.hero.y += 50
        elif keycode[1] == 'down':
            self.ids.hero.y -= 50
        else:
            return False
        return True




class NewScreen(Screen):
    if_then = False
    joystick = Joystick(0, True)

    def __init__(self, **kwargs):
        Builder.load_file('NewScreen.kv')
        super(NewScreen, self).__init__(**kwargs)

    def thread_function(self):
        y = threading.Thread(target=self.joystick1, daemon=True)
        y.start()

    def joystick1(self):
        while True:

            self.ids.location.x = self.joystick.get_axis('x') * (self.width / 2)
            self.ids.location.y = self.joystick.get_axis('y') * -(self.height / 2)
            self.ids.location.text = "{:.3f} {:1.3f}".format(self.joystick.get_axis('x'), (self.joystick.get_axis('y')))

            for x in range(11):
                if self.joystick.get_button_state(x) == 1:
                    self.ids.updates.text = str(x)
                    break
                else:
                    self.ids.updates.text = "No button depressed"

            if (-.9 * (self.width / 2)) <= self.ids.location.x <= (-.5 * (self.width / 2)) and \
               (-.4 * (self.height / 2)) <= self.ids.location.y <= (-.0001 * (self.height / 2)):
                pass
            else:
                self.ids.on.text = "Not Pressed"


            if (-.9 * (self.width / 2)) <= self.ids.location.x <= (-.5 * (self.width / 2)) and \
                    (-.4 * (self.height / 2)) <= self.ids.location.y <= (-.0001 * (self.height / 2)) and \
                    self.joystick.get_button_state(0) == 0 and self.if_then == False:
                self.if_then = True
                self.ids.on.text = "Not Pressed"



            if (-.9 * (self.width / 2)) <= self.ids.location.x <= (-.5 * (self.width / 2)) and \
                    (-.4 * (self.height / 2)) <= self.ids.location.y <= (-.0001 * (self.height / 2)) and \
                    self.if_then and self.joystick.get_button_state(0) == 1:
                self.ids.on.text = "Pressed!"
                self.if_then = False


            time.sleep(.1)

    def mainscreen(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def animation(self):

        self.anim = Animation(x=50, y=100, duration=2.) & Animation(size=(200, 200), duration=2.)

        for w in range(3):
            self.anim += Animation(x=750, y=300, duration=.05) & Animation(size=(50, 50), duration=.05)
            self.anim += Animation(x=200, y=600, duration=.05) & Animation(size=(500, 500), duration=.05)
            self.anim += Animation(x=5, y=300, duration=.05) & Animation(size=(200, 200), duration=.05)
            self.anim += Animation(x=600, y=10, duration=.05) & Animation(size=(10, 10), duration=.05)

        self.anim += Animation(x=400, y=75, duration=2.) & Animation(size=(120, 120), duration=2.)
        self.anim.start(self.ids.animation)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))
SCREEN_MANAGER.add_widget(Game(name=GAME_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
