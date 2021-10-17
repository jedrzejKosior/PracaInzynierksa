from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import psycopg2

# #############################DATABASE START#############################

# connect to database
conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
# connection = psycopg2.connect('hotel.db')

# cursor
cur = conn.cursor()

# cur.execute("CREATE TABLE clients
# (first_name text,last_name text,address text,city text,state text,zipcode text,room_number integer)")
# cur.execute("INSERT INTO clients VALUES
# ('Klaudia', 'Kromolowska', 'ul. Gminna 89', 'Czestochowa', 'Slask', '11-222', '5')")


# commit your changes
conn.commit()

# close cursor
cur.close()

# close connection
conn.close()

# ################ DATABASE END #############

# Name of style file
Builder.load_file('login_page.kv')
Window.minimum_width, Window.minimum_height = 500, 560


class MyLayout(Widget):
    login = ObjectProperty(None)
    password = ObjectProperty(None)

    def press(self):
        login = self.login.text
        password = self.password.text
        print(f"Hello {login}, {password}")
        # update button label
        # self.ids.printName.text = f'Hello {login}!'
        # Clear input
        self.login.text = ""
        self.password.text = ""


class Application(App):
    def build(self):
        # background color
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return MyLayout()


if __name__ == '__main__':
    Application().run()
