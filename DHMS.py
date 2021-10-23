from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import psycopg2

# cur.execute("CREATE TABLE users(userName text,password text)")
# cur.execute("INSERT INTO users VALUES('reception1', 'admin1234')")

Window.minimum_width, Window.minimum_height = 500, 560


# Define our different screens
class LoginWindow(Screen):
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    window = "loginWindow"

    def loginPress(self):
        # connect to database
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
        # cursor
        cur = conn.cursor()

        login = self.login.text
        password = self.password.text
        cur.execute("SELECT * from users")
        userData = cur.fetchall()
        foundLogin = False
        for user in userData:
            if login == user[0]:
                foundLogin = True
                if password == user[1]:
                    self.window = "registerWindow"
                else:
                    self.ids.passwordLabel.text = 'INCORRECT PASSWORD!'
                    self.ids.passwordLabel.color = (163 / 255, 22 / 255, 33 / 255, 1)
                break
        if not foundLogin:
            self.ids.loginLabel.text = 'INCORRECT LOGIN!'
            self.ids.loginLabel.color = (163 / 255, 22 / 255, 33 / 255, 1)

        # print(f"Hello {login}, {password}")
        # commit your changes
        conn.commit()
        # close cursor
        cur.close()
        # close connection
        conn.close()
        # update button label
        # self.ids.printName.text = f'Hello {login}!'
        # Clear input
        self.login.text = ""
        self.password.text = ""
        return self.window


class RegisterWindow(Screen):
    firstName = ObjectProperty(None)

    def registerPress(self):
        print(self.ids.firstName.text)


class WindowManager(ScreenManager):
    pass


# Name of style file
kv = Builder.load_file('login_page.kv')


class DesktopHotelManagementSystem(App):

    def build(self):
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return kv


if __name__ == '__main__':
    DesktopHotelManagementSystem().run()
