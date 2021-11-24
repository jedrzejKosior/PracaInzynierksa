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

Window.minimum_width, Window.minimum_height = 800, 580


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
                    self.window = "bookWindow"
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
        DesktopHotelManagementSystem.startDayOutput = self.ids.startDay.text
        DesktopHotelManagementSystem.startMonthOutput = self.ids.startMonth.text
        DesktopHotelManagementSystem.startYearOutput = self.ids.startYear.text
        DesktopHotelManagementSystem.endDayOutput = self.ids.endDay.text
        DesktopHotelManagementSystem.endMonthOutput = self.ids.endMonth.text
        DesktopHotelManagementSystem.endYearOutput = self.ids.endYear.text
        return 'roomWindow'


class RoomWindow(Screen):
    isSelected = False

    def selectedRoom1(self):
        if self.ids.room1.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(1)
            self.ids.room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room1.background_color[0] < 0.57:
            self.ids.room1.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(1)

    def selectedRoom2(self):
        if self.ids.room2.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(2)
            self.ids.room2.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room2.background_color[0] < 0.57:
            self.ids.room2.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(2)

    def selectedRoom3(self):
        if self.ids.room3.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(3)
            self.ids.room3.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room3.background_color[0] < 0.57:
            self.ids.room3.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(3)

    def selectedRoom4(self):
        if self.ids.room4.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(4)
            self.ids.room4.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room4.background_color[0] < 0.57:
            self.ids.room4.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(4)

    def selectedRoom5(self):
        if self.ids.room5.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(5)
            self.ids.room5.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room5.background_color[0] < 0.57:
            self.ids.room5.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(5)

    def selectedRoom6(self):
        if self.ids.room6.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(6)
            self.ids.room6.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room6.background_color[0] < 0.57:
            self.ids.room6.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(6)

    def selectedRoom7(self):
        if self.ids.room7.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(7)
            self.ids.room7.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room7.background_color[0] < 0.57:
            self.ids.room7.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(7)

    def selectedRoom8(self):
        if self.ids.room8.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(8)
            self.ids.room8.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room8.background_color[0] < 0.57:
            self.ids.room8.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(8)

    def selectedRoom9(self):
        if self.ids.room9.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(9)
            self.ids.room9.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room9.background_color[0] < 0.57:
            self.ids.room9.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(9)

    def selectedRoom10(self):
        if self.ids.room10.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(10)
            self.ids.room10.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room10.background_color[0] < 0.57:
            self.ids.room10.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(10)

    def selectedRoom11(self):
        if self.ids.room11.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(11)
            self.ids.room11.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room11.background_color[0] < 0.57:
            self.ids.room11.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(11)

    def selectedRoom12(self):
        if self.ids.room12.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(12)
            self.ids.room12.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room12.background_color[0] < 0.57:
            self.ids.room12.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(12)

    def selectedRoom13(self):
        if self.ids.room13.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(13)
            self.ids.room13.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room13.background_color[0] < 0.57:
            self.ids.room13.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(13)

    def selectedRoom14(self):
        if self.ids.room14.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(14)
            self.ids.room14.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room14.background_color[0] < 0.57:
            self.ids.room14.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(14)

    def selectedRoom15(self):
        if self.ids.room15.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(15)
            self.ids.room15.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room15.background_color[0] < 0.57:
            self.ids.room15.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(15)

    def selectedRoom16(self):
        if self.ids.room16.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(16)
            self.ids.room16.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room16.background_color[0] < 0.57:
            self.ids.room16.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(16)

    def selectedRoom17(self):
        if self.ids.room17.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(17)
            self.ids.room17.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room17.background_color[0] < 0.57:
            self.ids.room17.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(17)

    def selectedRoom18(self):
        if self.ids.room18.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(18)
            self.ids.room18.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room18.background_color[0] < 0.57:
            self.ids.room18.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(18)

    def selectedRoom19(self):
        if self.ids.room19.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(19)
            self.ids.room19.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room19.background_color[0] < 0.57:
            self.ids.room19.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(19)

    def selectedRoom20(self):
        if self.ids.room20.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(20)
            self.ids.room20.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room20.background_color[0] < 0.57:
            self.ids.room20.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(20)


class BookWindow(Screen):
    def registerPress(self):
        DesktopHotelManagementSystem.clientInformation.append(self.ids.firstName.text)
        DesktopHotelManagementSystem.clientInformation.append(self.ids.secondName.text)
        DesktopHotelManagementSystem.clientInformation.append(self.ids.email.text)
        DesktopHotelManagementSystem.clientInformation.append(self.ids.telephone.text)
        print(DesktopHotelManagementSystem.clientInformation)

    def is_not_right_name_city_state(self, textInput):
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


class WindowManager(ScreenManager):
    pass


# Name of style file
kv = Builder.load_file('design.kv')


class DesktopHotelManagementSystem(App):
    startDayOutput = ""
    endDayOutput = ""
    startMonthOutput = ""
    endMonthOutput = ""
    startYearOutput = ""
    endYearOutput = ""
    selectedRoomNumbers = []
    clientInformation = []

    def build(self):
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return kv


if __name__ == '__main__':
    DesktopHotelManagementSystem().run()
