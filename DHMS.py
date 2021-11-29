from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.metrics import dp
from datetime import datetime
from calendar import monthrange
import psycopg2
import re

Window.minimum_width, Window.minimum_height = 800, 600


# validations of inputs
def isRightName(textInput):
    if len(textInput) == 0:
        return False
    if not textInput[0].isupper():
        return False
    for i in range(len(textInput)):
        if not textInput[i].isalpha():
            return False
    return True


def isRightTelephoneNumber(number):
    if len(number) != 9 and len(number) != 12:
        return False
    if len(number) == 9:
        for i in range(len(number)):
            if not number[i].isdigit():
                return False
    else:
        if number[0] == '+':
            i = 1
            while i < len(number):
                if not number[i].isdigit():
                    return False
                i = i + 1
        else:
            return False
    return True


def isRightEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
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
                    self.window = "actionWindow"
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
        self.password.text = ""
        return isCorrect, self.window


class ActionWindow(Screen):
    pass


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

    def resetToDefaults(self):
        self.manager.get_screen('dateWindow').startDay.text = DateWindow.currentDay
        self.manager.get_screen('dateWindow').startMonth.text = DateWindow.months[DateWindow.currentMonth - 1]
        self.manager.get_screen('dateWindow').startYear.text = DateWindow.currentYear

        self.manager.get_screen('dateWindow').endDay.text = DateWindow.currentDay
        self.manager.get_screen('dateWindow').endMonth.text = DateWindow.months[DateWindow.currentMonth - 1]
        self.manager.get_screen('dateWindow').endYear.text = DateWindow.currentYear

        self.manager.get_screen('roomWindow').room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room2.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room3.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room4.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room5.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room6.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room7.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room8.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room9.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room10.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room11.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room12.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room13.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room14.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room15.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room16.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room17.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room18.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room19.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room20.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        self.manager.get_screen('roomWindowFloor2').room21.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room22.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room23.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room24.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room25.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room26.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room27.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room28.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room29.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room30.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        self.manager.get_screen('bookWindow').firstName.text = ""
        self.manager.get_screen('bookWindow').lastName.text = ""
        self.manager.get_screen('bookWindow').email.text = ""
        self.manager.get_screen('bookWindow').telephone.text = ""

        DesktopHotelManagementSystem.startDayOutput = ""
        DesktopHotelManagementSystem.endDayOutput = ""
        DesktopHotelManagementSystem.startMonthOutput = ""
        DesktopHotelManagementSystem.endMonthOutput = ""
        DesktopHotelManagementSystem.startYearOutput = ""
        DesktopHotelManagementSystem.endYearOutput = ""
        DesktopHotelManagementSystem.selectedRoomNumbers = []
        DesktopHotelManagementSystem.clientInformation = []
        DesktopHotelManagementSystem.startDateToCheckColor = ""
        DesktopHotelManagementSystem.endDateToCheckColor = ""

        return "actionWindow"

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
        DesktopHotelManagementSystem.startDateToCheckColor, DesktopHotelManagementSystem.endDateToCheckColor = \
            dataParsing()
        return 'roomWindow'


def turnRedIfUnavailable():
    startDate = DesktopHotelManagementSystem.startDateToCheckColor
    endDate = DesktopHotelManagementSystem.endDateToCheckColor
    # connect to database
    conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
    # cursor
    cur = conn.cursor()
    unavailableRooms = []
    for roomNumber in range(30):
        cur.execute("SELECT startDate, endDate FROM room" + str(roomNumber + 1))
        roomsDates = cur.fetchall()
        for roomPeriod in roomsDates:
            if (int(roomPeriod[0]) <= int(startDate) < int(roomPeriod[1])) or (
                    int(roomPeriod[0]) < int(endDate) <= int(roomPeriod[1])) or (
                    int(startDate) <= int(roomPeriod[0]) and int(endDate) >= int(roomPeriod[1])):
                unavailableRooms.append(roomNumber + 1)
    conn.commit()
    # close cursor
    cur.close()
    # close connection
    conn.close()
    return unavailableRooms


def dataParsing():
    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
              "NOVEMBER", "DECEMBER"]
    if int(months.index(DesktopHotelManagementSystem.startMonthOutput) + 1) < 10:
        startMonthToDatabase = str(0) + str(
            int(months.index(DesktopHotelManagementSystem.startMonthOutput) + 1))
    else:
        startMonthToDatabase = str(int(months.index(DesktopHotelManagementSystem.startMonthOutput) + 1))
    if int(DesktopHotelManagementSystem.startDayOutput) < 10:
        startDayToDatabase = str(0) + str(int(DesktopHotelManagementSystem.startDayOutput))
    else:
        startDayToDatabase = str(int(DesktopHotelManagementSystem.startDayOutput))

    if int(months.index(DesktopHotelManagementSystem.endMonthOutput) + 1) < 10:
        endMonthToDatabase = str(0) + str(
            int(months.index(DesktopHotelManagementSystem.endMonthOutput) + 1))
    else:
        endMonthToDatabase = str(int(months.index(DesktopHotelManagementSystem.endMonthOutput)) + 1)
    if int(DesktopHotelManagementSystem.endDayOutput) < 10:
        endDayToDatabase = str(0) + str(int(DesktopHotelManagementSystem.endDayOutput))
    else:
        endDayToDatabase = str(int(DesktopHotelManagementSystem.endDayOutput))
    startDateToCheckColor = str(
        DesktopHotelManagementSystem.startYearOutput) + startMonthToDatabase + startDayToDatabase
    endDateToCheckColor = str(DesktopHotelManagementSystem.endYearOutput) + endMonthToDatabase + endDayToDatabase
    return startDateToCheckColor, endDateToCheckColor


class RoomWindow(Screen):
    def makeRedColors(self):
        if 0.63 < self.ids.room1.background_color[0] < 0.64:
            self.ids.room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room2.background_color[0] < 0.64:
            self.ids.room2.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room3.background_color[0] < 0.64:
            self.ids.room3.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room4.background_color[0] < 0.64:
            self.ids.room4.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room5.background_color[0] < 0.64:
            self.ids.room5.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room6.background_color[0] < 0.64:
            self.ids.room6.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room7.background_color[0] < 0.64:
            self.ids.room7.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room8.background_color[0] < 0.64:
            self.ids.room8.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room9.background_color[0] < 0.64:
            self.ids.room9.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room10.background_color[0] < 0.64:
            self.ids.room10.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room11.background_color[0] < 0.64:
            self.ids.room11.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room12.background_color[0] < 0.64:
            self.ids.room12.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room13.background_color[0] < 0.64:
            self.ids.room13.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room14.background_color[0] < 0.64:
            self.ids.room14.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room15.background_color[0] < 0.64:
            self.ids.room15.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room16.background_color[0] < 0.64:
            self.ids.room16.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room17.background_color[0] < 0.64:
            self.ids.room17.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room18.background_color[0] < 0.64:
            self.ids.room18.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room19.background_color[0] < 0.64:
            self.ids.room19.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room20.background_color[0] < 0.64:
            self.ids.room20.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        unavailableRooms = turnRedIfUnavailable()
        for room in unavailableRooms:
            if room in DesktopHotelManagementSystem.selectedRoomNumbers:
                DesktopHotelManagementSystem.selectedRoomNumbers.remove(room)
            if room == 1:
                self.ids.room1.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 2:
                self.ids.room2.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 3:
                self.ids.room3.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 4:
                self.ids.room4.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 5:
                self.ids.room5.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 6:
                self.ids.room6.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 7:
                self.ids.room7.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 8:
                self.ids.room8.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 9:
                self.ids.room9.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 10:
                self.ids.room10.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 11:
                self.ids.room11.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 12:
                self.ids.room12.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 13:
                self.ids.room13.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 14:
                self.ids.room14.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 15:
                self.ids.room15.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 16:
                self.ids.room16.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 17:
                self.ids.room17.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 18:
                self.ids.room18.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 19:
                self.ids.room19.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 20:
                self.ids.room20.background_color = (163 / 255, 22 / 255, 33 / 255, 1)

    def selectedRoom1(self):
        if self.ids.room1.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(1)
            self.ids.room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room1.background_color[0] < 0.57:  # if blue
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


class RoomWindowFloor2(Screen):
    def makeRedColorsFloor2(self):
        if 0.63 < self.ids.room21.background_color[0] < 0.64:
            self.ids.room21.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room22.background_color[0] < 0.64:
            self.ids.room22.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room23.background_color[0] < 0.64:
            self.ids.room23.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room24.background_color[0] < 0.64:
            self.ids.room24.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room25.background_color[0] < 0.64:
            self.ids.room25.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room26.background_color[0] < 0.64:
            self.ids.room26.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room27.background_color[0] < 0.64:
            self.ids.room27.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room28.background_color[0] < 0.64:
            self.ids.room28.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room29.background_color[0] < 0.64:
            self.ids.room29.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        if 0.63 < self.ids.room30.background_color[0] < 0.64:
            self.ids.room30.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        unavailableRooms = turnRedIfUnavailable()
        for room in unavailableRooms:
            if room in DesktopHotelManagementSystem.selectedRoomNumbers:
                DesktopHotelManagementSystem.selectedRoomNumbers.remove(room)
            if room == 21:
                self.ids.room21.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 22:
                self.ids.room22.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 23:
                self.ids.room23.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 24:
                self.ids.room24.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 25:
                self.ids.room25.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 26:
                self.ids.room26.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 27:
                self.ids.room27.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 28:
                self.ids.room28.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 29:
                self.ids.room29.background_color = (163 / 255, 22 / 255, 33 / 255, 1)
            if room == 30:
                self.ids.room30.background_color = (163 / 255, 22 / 255, 33 / 255, 1)

    def selectedRoom21(self):
        if self.ids.room21.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(21)
            self.ids.room21.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room21.background_color[0] < 0.57:
            self.ids.room21.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(21)

    def selectedRoom22(self):
        if self.ids.room22.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(22)
            self.ids.room22.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room22.background_color[0] < 0.57:
            self.ids.room22.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(22)

    def selectedRoom23(self):
        if self.ids.room23.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(23)
            self.ids.room23.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room23.background_color[0] < 0.57:
            self.ids.room23.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(23)

    def selectedRoom24(self):
        if self.ids.room24.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(24)
            self.ids.room24.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room24.background_color[0] < 0.57:
            self.ids.room24.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(24)

    def selectedRoom25(self):
        if self.ids.room25.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(25)
            self.ids.room25.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room25.background_color[0] < 0.57:
            self.ids.room25.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(25)

    def selectedRoom26(self):
        if self.ids.room26.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(26)
            self.ids.room26.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room26.background_color[0] < 0.57:
            self.ids.room6.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(26)

    def selectedRoom27(self):
        if self.ids.room27.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(27)
            self.ids.room27.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room27.background_color[0] < 0.57:
            self.ids.room27.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(27)

    def selectedRoom28(self):
        if self.ids.room28.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(28)
            self.ids.room28.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room28.background_color[0] < 0.57:
            self.ids.room28.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(28)

    def selectedRoom29(self):
        if self.ids.room29.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(29)
            self.ids.room29.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room29.background_color[0] < 0.57:
            self.ids.room29.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(29)

    def selectedRoom30(self):
        if self.ids.room30.background_color[0] == 0:  # if green
            DesktopHotelManagementSystem.selectedRoomNumbers.remove(30)
            self.ids.room30.background_color = (144 / 255, 194 / 255, 231 / 255, 1)  # then blue
        elif 0.55 < self.ids.room30.background_color[0] < 0.57:
            self.ids.room30.background_color = (0, 224 / 255, 161 / 255, 1)  # else green
            DesktopHotelManagementSystem.selectedRoomNumbers.append(30)


class BookWindow(Screen):
    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
              "NOVEMBER", "DECEMBER"]

    def resetToDefaults(self):
        self.manager.get_screen('dateWindow').startDay.text = DateWindow.currentDay
        self.manager.get_screen('dateWindow').startMonth.text = DateWindow.months[DateWindow.currentMonth - 1]
        self.manager.get_screen('dateWindow').startYear.text = DateWindow.currentYear

        self.manager.get_screen('dateWindow').endDay.text = DateWindow.currentDay
        self.manager.get_screen('dateWindow').endMonth.text = DateWindow.months[DateWindow.currentMonth - 1]
        self.manager.get_screen('dateWindow').endYear.text = DateWindow.currentYear

        self.manager.get_screen('roomWindow').room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room2.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room3.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room4.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room5.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room6.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room7.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room8.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room9.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room10.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room11.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room12.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room13.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room14.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room15.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room16.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room17.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room18.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room19.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindow').room20.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        self.manager.get_screen('roomWindowFloor2').room21.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room22.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room23.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room24.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room25.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room26.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room27.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room28.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room29.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        self.manager.get_screen('roomWindowFloor2').room30.background_color = (144 / 255, 194 / 255, 231 / 255, 1)

        self.manager.get_screen('bookWindow').firstName.text = ""
        self.manager.get_screen('bookWindow').lastName.text = ""
        self.manager.get_screen('bookWindow').email.text = ""
        self.manager.get_screen('bookWindow').telephone.text = ""

        DesktopHotelManagementSystem.startDayOutput = ""
        DesktopHotelManagementSystem.endDayOutput = ""
        DesktopHotelManagementSystem.startMonthOutput = ""
        DesktopHotelManagementSystem.endMonthOutput = ""
        DesktopHotelManagementSystem.startYearOutput = ""
        DesktopHotelManagementSystem.endYearOutput = ""
        DesktopHotelManagementSystem.selectedRoomNumbers = []
        DesktopHotelManagementSystem.clientInformation = []
        DesktopHotelManagementSystem.startDateToCheckColor = ""
        DesktopHotelManagementSystem.endDateToCheckColor = ""

    def registerPress(self):
        if isRightName(self.ids.firstName.text) and isRightName(self.ids.lastName.text) and isRightEmail(
                self.ids.email.text) and isRightTelephoneNumber(self.ids.telephone.text):
            DesktopHotelManagementSystem.clientInformation.append(self.ids.firstName.text)
            DesktopHotelManagementSystem.clientInformation.append(self.ids.lastName.text)
            DesktopHotelManagementSystem.clientInformation.append(self.ids.email.text)
            DesktopHotelManagementSystem.clientInformation.append(self.ids.telephone.text)
            # connect to database
            conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
            # cursor
            cur = conn.cursor()
            cur.execute("SELECT MAX(clientID) FROM clients")
            maxID = cur.fetchall()[0][0]
            if maxID is None:
                maxID = 1
            else:
                maxID = int(maxID) + 1
            cur.execute("SELECT clientID FROM clients WHERE email = '" + DesktopHotelManagementSystem.clientInformation[
                2] + "' AND telephone = '" + DesktopHotelManagementSystem.clientInformation[3] + "'")
            existedClientID = cur.fetchall()
            if len(existedClientID):
                selectedID = existedClientID[0][0]
            else:
                selectedID = maxID
                cur.execute(
                    "INSERT INTO clients VALUES('" + DesktopHotelManagementSystem.clientInformation[0] + "', '" +
                    DesktopHotelManagementSystem.clientInformation[1] + "', '" +
                    DesktopHotelManagementSystem.clientInformation[2] + "', '" +
                    DesktopHotelManagementSystem.clientInformation[3] + "', '" + str(selectedID) + "')")
                conn.commit()
            if int(self.months.index(DesktopHotelManagementSystem.startMonthOutput) + 1) < 10:
                startMonthToDatabase = str(0) + str(
                    int(self.months.index(DesktopHotelManagementSystem.startMonthOutput) + 1))
            else:
                startMonthToDatabase = str(int(self.months.index(DesktopHotelManagementSystem.startMonthOutput) + 1))
            if int(DesktopHotelManagementSystem.startDayOutput) < 10:
                startDayToDatabase = str(0) + str(int(DesktopHotelManagementSystem.startDayOutput))
            else:
                startDayToDatabase = str(int(DesktopHotelManagementSystem.startDayOutput))

            if int(self.months.index(DesktopHotelManagementSystem.endMonthOutput) + 1) < 10:
                endMonthToDatabase = str(0) + str(
                    int(self.months.index(DesktopHotelManagementSystem.endMonthOutput) + 1))
            else:
                endMonthToDatabase = str(int(self.months.index(DesktopHotelManagementSystem.endMonthOutput)) + 1)
            if int(DesktopHotelManagementSystem.endDayOutput) < 10:
                endDayToDatabase = str(0) + str(int(DesktopHotelManagementSystem.endDayOutput))
            else:
                endDayToDatabase = str(int(DesktopHotelManagementSystem.endDayOutput))

            for room in DesktopHotelManagementSystem.selectedRoomNumbers:
                cur.execute("INSERT INTO room" + str(room) + " VALUES('" + str(
                    room) + "', '" + DesktopHotelManagementSystem.startYearOutput + startMonthToDatabase +
                            startDayToDatabase + "', '" + DesktopHotelManagementSystem.endYearOutput +
                            endMonthToDatabase + endDayToDatabase + "', '" + str(selectedID) + "')")
            conn.commit()
            # close cursor
            cur.close()
            # close connection
            conn.close()

            return True
        else:
            return False


class BrowserWindow(Screen):
    pageLimits = [0, 10]

    def createBooksRows(self):
        # connect to database
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
        # cursor
        cur = conn.cursor()
        dataToBrowse = []
        for roomNumber in range(30):
            cur.execute(
                "SELECT room" + str(roomNumber + 1) + ".roomnumber, clients.lastname, clients.email, room" + str(
                    roomNumber + 1) + ".startdate, room" + str(
                    roomNumber + 1) + ".enddate FROM clients JOIN room" + str(
                    roomNumber + 1) + " ON clients.clientid = room" + str(
                    roomNumber + 1) + ".clientid ORDER BY room" + str(roomNumber + 1) + ".startdate, room" + str(
                    roomNumber + 1) + ".clientid, room" + str(roomNumber + 1) + ".enddate")
            dataN = cur.fetchall()
            if len(dataN) > 0:
                dataToBrowse.append(dataN)
        conn.commit()
        # close cursor
        cur.close()
        # close connection
        conn.close()

        buttonsLayout = BoxLayout(orientation="horizontal")
        buttonsLayout.add_widget(Button(text="BACK", on_relese=))
        buttonsLayout.add_widget(TextInput(hint_text="LAST NAME, EMAIL, ETC.", size_hint_y=None, height=41))
        buttonsLayout.add_widget(
            Spinner(text="CATEGORY", values=["ROOM", "LAST NAME", "E-MAIL", "START DATE", "END DATE"], size_hint_y=None, height=40))
        buttonsLayout.add_widget(
            Button(text="SEARCH", background_color=(163 / 255, 22 / 255, 33 / 255, 1), color=(1, 1, 1, 1), size_hint_y=None, height=40))

        header = GridLayout(padding=[30, 0, 30, 0], cols=6, spacing=20)
        header.add_widget(Label(text="ROOM", color=(0, 0, 0, 1), size_hint_x=None, width=50))
        header.add_widget(Label(text="LAST NAME", color=(0, 0, 0, 1)))
        header.add_widget(Label(text="E-MAIL", color=(0, 0, 0, 1)))
        header.add_widget(Label(text="START DATE", color=(0, 0, 0, 1), size_hint_x=None, width=90))
        header.add_widget(Label(text="END DATE", color=(0, 0, 0, 1), size_hint_x=None, width=90))
        header.add_widget(Label(text="UPDATE", color=(0, 0, 0, 1), size_hint_x=None, width=60))

        layout = GridLayout(padding=30, cols=6, spacing=20, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(dataToBrowse)):
            oneRoomData = dataToBrowse[i]
            for j in oneRoomData:
                startDate = j[3][6:] + "-" + j[3][4:6] + "-" + j[3][:4]
                endDate = j[4][6:] + "-" + j[4][4:6] + "-" + j[4][:4]
                layout.add_widget(Label(text=str(j[0]), color=(0, 0, 0, 1), size_hint_x=None, width=50))
                layout.add_widget(Label(text=str(j[1]), color=(0, 0, 0, 1)))
                layout.add_widget(Label(text=str(j[2]), color=(0, 0, 0, 1)))
                layout.add_widget(Label(text=startDate, color=(0, 0, 0, 1), size_hint_x=None, width=90))
                layout.add_widget(Label(text=endDate, color=(0, 0, 0, 1), size_hint_x=None, width=90))
                layout.add_widget(
                    Button(text="SELECT", color=(0, 0, 0, 1), background_color=(144 / 255, 194 / 255, 231 / 255, 1),
                           size_hint_y=None, height=30, size_hint_x=None, width=60))  # TODO this must be normal implementation
        scrollRoot = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.80))
        scrollRoot.add_widget(layout)
        mainLayout = BoxLayout(padding=30, orientation="vertical")
        mainLayout.add_widget(header)
        mainLayout.add_widget(scrollRoot)
        mainLayout.add_widget(buttonsLayout)
        self.add_widget(mainLayout)
        # self.add_widget(scrollRoot)


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
    startDateToCheckColor = ""
    endDateToCheckColor = ""

    def build(self):
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return kv


if __name__ == '__main__':
    DesktopHotelManagementSystem().run()
