from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.metrics import dp
from datetime import datetime
from calendar import monthrange
import psycopg2

# cur.execute("CREATE TABLE users(userName text,password text)")
# cur.execute("INSERT INTO users VALUES('reception1', 'admin1234')")

Window.minimum_width, Window.minimum_height = 500, 580


# validations of inputs

# def is_already_taken_for_update(room_number, starting_date, ending_date, client):
#     conn = psycopg2.connect('hotel.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT book_start, book_end, client_id FROM room" + str(room_number))
#     status_checking = cursor.fetchall()
#
#     # commit changes
#     conn.commit()
#
#     # close connection
#     conn.close()
#     i = 0
#     # for i in range(len(status_checking)):
#     while (i < len(status_checking)):
#         if ((starting_date >= status_checking[i][0] and starting_date < status_checking[i][1]) or (
#                 ending_date > status_checking[i][0] and ending_date <= status_checking[i][1]) or (
#                 starting_date <= status_checking[i][0] and ending_date >= status_checking[i][1])):
#             if (int(client) == int(status_checking[i][2])):
#                 i = i + 1
#                 continue
#             else:
#                 return True
#         i = i + 1
#     return False
#
#
# def is_already_taken(room_number, starting_date, ending_date):
#     conn = psycopg2.connect('hotel.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT book_start, book_end, client_id FROM room" + str(room_number))
#     status_checking = cursor.fetchall()
#
#     # commit changes
#     conn.commit()
#
#     # close connection
#     conn.close()
#     i = 0
#     # for i in range(len(status_checking)):
#     while (i < len(status_checking)):
#         if ((starting_date >= status_checking[i][0] and starting_date < status_checking[i][1]) or (
#                 ending_date > status_checking[i][0] and ending_date <= status_checking[i][1]) or (
#                 starting_date <= status_checking[i][0] and ending_date >= status_checking[i][1])):
#             return True
#         i = i + 1
#     return False


def is_not_right_zipcode(textInput):
    if len(textInput) == 0 or len(textInput) != 6:
        return True
    if textInput[2] != "-":
        return True
    for i in range(len(textInput)):
        if i == 2:
            i = i + 1
        if textInput[i].isdigit():
            continue
        else:
            return True
    return False


def is_not_right_name_city_state(textInput):
    if len(textInput) == 0:
        return True
    if not textInput[0].isupper():
        return True
    for i in range(len(textInput)):
        if textInput[i].isalpha():
            continue
        else:
            return True
    return False


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

        isCorrect = True
        login = self.login.text
        password = self.password.text
        cur.execute("SELECT * from users")
        userData = cur.fetchall()
        foundLogin = False
        for user in userData:
            if login == user[0]:
                foundLogin = True
                if password == user[1]:
                    self.window = "dateWindow"
                else:
                    isCorrect = False
                break
        if not foundLogin:
            isCorrect = False

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
        return isCorrect, self.window


class DateWindow(Screen):
    startDay = ObjectProperty(None)
    endDay = ObjectProperty(None)
    startMonth = ObjectProperty(None)
    endMonth = ObjectProperty(None)
    startYear = ObjectProperty(None)
    endYear = ObjectProperty(None)

    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
              "NOVEMBER", "DECEMBER"]

    currentYear = str(datetime.now().year)
    currentMonth = datetime.now().month
    currentDay = str(datetime.now().day)
    daysStart = []
    for i in range(monthrange(int(currentYear), currentMonth)[1]):
        daysStart.append(str(i + 1))
    daysEnd = daysStart.copy()

    def daysInSelectedMonthForStart(self):
        self.daysStart = []
        for i in range(monthrange(int(self.ids.startYear.text), self.months.index(self.ids.startMonth.text) + 1)[1]):
            self.daysStart.append(str(i + 1))
        self.startDay.values = self.daysStart
        if int(self.startDay.text) > int(self.daysStart[-1]):
            self.startDay.text = str(self.daysStart[-1])

    def daysInSelectedMonthForEnd(self):
        self.daysEnd = []
        for i in range(monthrange(int(self.ids.endYear.text), self.months.index(self.ids.endMonth.text) + 1)[1]):
            self.daysEnd.append(str(i + 1))
        self.endDay.values = self.daysEnd
        if int(self.endDay.text) > int(self.daysEnd[-1]):
            self.endDay.text = str(self.daysEnd[-1])

    def limit_spinner(self):
        maxItems = 3
        self.spinner.dropdown_cls.max_height = maxItems * dp(48)

    def wrongTimePeriod(self):
        isCorrect = True
        if int(self.ids.startYear.text) > int(self.ids.endYear.text):
            isCorrect = False
        if (self.months.index(self.ids.startMonth.text) > self.months.index(self.ids.endMonth.text)) and (
                int(self.ids.startYear.text) >= int(self.ids.endYear.text)):
            isCorrect = False
        if (int(self.ids.startDay.text) >= int(self.ids.endDay.text)) and (
                self.months.index(self.ids.startMonth.text) >= self.months.index(self.ids.endMonth.text)) and (
                int(self.ids.startYear.text) >= int(self.ids.endYear.text)):
            isCorrect = False
        return isCorrect

    def searchPress(self):
        pass


class RegisterWindow(Screen):
    firstName = ObjectProperty(None)

    def registerPress(self):
        print(self.ids.firstName.text)
        print(self.ids.status.text)

    def spinnerClicked(self, value):
        self.ids.status.text = value

    def limit_spinner(self):
        maxItems = 3
        self.spinner.dropdown_cls.max_height = maxItems * dp(48)


class WindowManager(ScreenManager):
    pass


# Name of style file
kv = Builder.load_file('design.kv')


class DesktopHotelManagementSystem(App):
    def build(self):
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return kv


if __name__ == '__main__':
    DesktopHotelManagementSystem().run()

# TODO change layout to accomplish step by step. On first register window, input room requirements such as START and END
# TODO DATES, room people size. If available proceed to ROOM GUI, select and hit next, input CLIENT data and REGISTER
