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
#     conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin)
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
#     conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin)
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
    if len(email) < 5:
        return False
    if "@" not in email or "." not in email:
        return False
    return True


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

        # if ((starting_date >= status_checking[i][0] and starting_date < status_checking[i][1]) or (
        #         ending_date > status_checking[i][0] and ending_date <= status_checking[i][1]) or (
        #         starting_date <= status_checking[i][0] and ending_date >= status_checking[i][1])):


def turnRedIfUnavailable(roomNumber, startDate, endDate):
    # connect to database
    conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
    # cursor
    cur = conn.cursor()
    cur.execute("SELECT startDate, endDate FROM room" + str(roomNumber))
    roomsDates = cur.fetchall()
    for roomPeriod in roomsDates:
        if (int(startDate) >= int(roomPeriod[0]) and int(startDate) < int(roomPeriod[1])) or (int(endDate) > int(roomPeriod[0]) and int(endDate) <= int(roomPeriod[1])) or (int(startDate) <= int(roomPeriod[0]) and int(endDate) >= int(roomPeriod[1])):
            print("dupa")  # TODO
    conn.commit()
    # close cursor
    cur.close()
    # close connection
    conn.close()


turnRedIfUnavailable(17, 20210101, 20211201)


class RoomWindow(Screen):
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


class RoomWindowFloor2(Screen):
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
