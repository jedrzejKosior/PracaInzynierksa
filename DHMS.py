from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.metrics import dp
from datetime import datetime, timedelta, date
from calendar import monthrange
import psycopg2
import re

Window.minimum_width, Window.minimum_height = 800, 600


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


class LoginWindow(Screen):
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    window = "loginWindow"

    def loginPress(self):
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
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
                    if user[2] == "reception":
                        self.window = "actionWindow"
                    elif user[2] == "kitchen":
                        self.window = "kitchenWindow"
                    elif user[2] == "maid":
                        self.window = "maidWindow"
                    else:
                        self.window = "adminWindow"
                else:
                    isCorrect = False
                break
        if not foundLogin:
            isCorrect = False
        conn.commit()
        cur.close()
        conn.close()
        self.password.text = ""
        return isCorrect, self.window


class ActionWindow(Screen):
    pass


class AdminWindow(Screen):
    def createUser(self):
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
        cur = conn.cursor()
        newUser = self.ids.newLogin.text
        newPassword = self.ids.newPassword.text
        newPermission = self.ids.permissions.text
        if len(newUser) == 0 or len(newPassword) == 0 or newPermission == "PERMISSIONS":
            return False
        cur.execute("SELECT username FROM users")
        users = cur.fetchall()
        for user in users:
            if user == newUser:
                return False
        cur.execute("INSERT INTO users VALUES ('" + str(newUser) + "', '" + str(newPassword) + "', '" + str(
            newPermission.lower() + "')"))
        conn.commit()
        cur.close()
        conn.close()
        self.ids.newLogin.text = ""
        self.ids.newPassword.text = ""
        self.ids.permissions.text = "PERMISSIONS"
        return True


class RoomWindowAbsence(Screen):
    # noinspection PyMethodMayBeStatic
    def parseDataToday(self):
        currentYear = str(datetime.now().year)
        currentMonth = str(datetime.now().month)
        currentDay = str(datetime.now().day)
        if int(currentMonth) < 10:
            startMonthToDatabase = str(0) + str(currentMonth)
        else:
            startMonthToDatabase = str(currentMonth)
        if int(currentDay) < 10:
            startDayToDatabase = str(0) + str(currentDay)
        else:
            startDayToDatabase = str(currentDay)

        dateToday = str(currentYear) + str(startMonthToDatabase) + str(startDayToDatabase)
        return dateToday

    def saveAbsence(self):
        dateToday = self.parseDataToday()
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")
        cur = conn.cursor()
        inputValue = self.ids.roomsInput.text
        inputLength = len(inputValue)
        if inputLength == 0:
            return False
        for index in range(inputLength):
            character = inputValue[index]
            if character.isdigit() or character == " " or character == ",":
                continue
            else:
                return False
        inputValue = re.sub(' +', ' ', inputValue)
        inputValue.replace(",", " ")
        inputValue.replace(", ", " ")
        rooms = inputValue.split()
        for i in rooms:
            if int(i) > 30:
                return False
            cur.execute("SELECT startdate, enddate FROM room" + str(i) + "")
            isRightDate = cur.fetchall()
            if len(isRightDate) == 0:
                return False
            flag = False
            for j in isRightDate:
                if int(j[0]) > int(dateToday) or int(j[1]) < int(dateToday):
                    continue
                else:
                    flag = True
                    break
            if not flag:
                return False
        if self.ids.statusInput.text == 'STATUS':
            return False
        for room in rooms:
            if self.ids.statusInput.text == 'ABSENT':
                cur.execute("UPDATE absence SET status = 'absent' WHERE roomnumber = '" + str(room) + "'")
            else:
                cur.execute("UPDATE absence SET status = 'present' WHERE roomnumber = '" + str(room) + "'")
        conn.commit()
        cur.close()

        conn.close()
        return True


class MaidWindow(Screen):
    def absentOrPresent(self):

        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        cur.execute("SELECT roomnumber, status FROM absence ORDER BY roomnumber")
        absentInfo = cur.fetchall()

        conn.commit()

        cur.close()

        conn.close()
        if absentInfo[0][1] == "present":
            self.ids.status1.text = "PRESENT"
            self.ids.status1.color = (0, 0, 0, 1)
        else:
            self.ids.status1.text = "ABSENT"
            self.ids.status1.color = (1, 1, 1, 1)
        if absentInfo[1][1] == "present":
            self.ids.status2.text = "PRESENT"
            self.ids.status2.color = (0, 0, 0, 1)
        else:
            self.ids.status2.text = "ABSENT"
            self.ids.status2.color = (1, 1, 1, 1)
        if absentInfo[2][1] == "present":
            self.ids.status3.text = "PRESENT"
            self.ids.status3.color = (0, 0, 0, 1)
        else:
            self.ids.status3.text = "ABSENT"
            self.ids.status3.color = (1, 1, 1, 1)
        if absentInfo[3][1] == "present":
            self.ids.status4.text = "PRESENT"
            self.ids.status4.color = (0, 0, 0, 1)
        else:
            self.ids.status4.text = "ABSENT"
            self.ids.status4.color = (1, 1, 1, 1)
        if absentInfo[4][1] == "present":
            self.ids.status5.text = "PRESENT"
            self.ids.status5.color = (0, 0, 0, 1)
        else:
            self.ids.status5.text = "ABSENT"
            self.ids.status5.color = (1, 1, 1, 1)
        if absentInfo[5][1] == "present":
            self.ids.status6.text = "PRESENT"
            self.ids.status6.color = (0, 0, 0, 1)
        else:
            self.ids.status6.text = "ABSENT"
            self.ids.status6.color = (1, 1, 1, 1)
        if absentInfo[6][1] == "present":
            self.ids.status7.text = "PRESENT"
            self.ids.status7.color = (0, 0, 0, 1)
        else:
            self.ids.status7.text = "ABSENT"
            self.ids.status7.color = (1, 1, 1, 1)
        if absentInfo[7][1] == "present":
            self.ids.status8.text = "PRESENT"
            self.ids.status8.color = (0, 0, 0, 1)
        else:
            self.ids.status8.text = "ABSENT"
            self.ids.status8.color = (1, 1, 1, 1)
        if absentInfo[8][1] == "present":
            self.ids.status9.text = "PRESENT"
            self.ids.status9.color = (0, 0, 0, 1)
        else:
            self.ids.status9.text = "ABSENT"
            self.ids.status9.color = (1, 1, 1, 1)
        if absentInfo[9][1] == "present":
            self.ids.status10.text = "PRESENT"
            self.ids.status10.color = (0, 0, 0, 1)
        else:
            self.ids.status10.text = "ABSENT"
            self.ids.status10.color = (1, 1, 1, 1)
        if absentInfo[10][1] == "present":
            self.ids.status11.text = "PRESENT"
            self.ids.status11.color = (0, 0, 0, 1)
        else:
            self.ids.status11.text = "ABSENT"
            self.ids.status11.color = (1, 1, 1, 1)
        if absentInfo[11][1] == "present":
            self.ids.status12.text = "PRESENT"
            self.ids.status12.color = (0, 0, 0, 1)
        else:
            self.ids.status12.text = "ABSENT"
            self.ids.status12.color = (1, 1, 1, 1)
        if absentInfo[12][1] == "present":
            self.ids.status13.text = "PRESENT"
            self.ids.status13.color = (0, 0, 0, 1)
        else:
            self.ids.status13.text = "ABSENT"
            self.ids.status13.color = (1, 1, 1, 1)
        if absentInfo[13][1] == "present":
            self.ids.status14.text = "PRESENT"
            self.ids.status14.color = (0, 0, 0, 1)
        else:
            self.ids.status14.text = "ABSENT"
            self.ids.status14.color = (1, 1, 1, 1)
        if absentInfo[14][1] == "present":
            self.ids.status15.text = "PRESENT"
            self.ids.status15.color = (0, 0, 0, 1)
        else:
            self.ids.status15.text = "ABSENT"
            self.ids.status15.color = (1, 1, 1, 1)
        if absentInfo[15][1] == "present":
            self.ids.status16.text = "PRESENT"
            self.ids.status16.color = (0, 0, 0, 1)
        else:
            self.ids.status16.text = "ABSENT"
            self.ids.status16.color = (1, 1, 1, 1)
        if absentInfo[16][1] == "present":
            self.ids.status17.text = "PRESENT"
            self.ids.status17.color = (0, 0, 0, 1)
        else:
            self.ids.status17.text = "ABSENT"
            self.ids.status17.color = (1, 1, 1, 1)
        if absentInfo[17][1] == "present":
            self.ids.status18.text = "PRESENT"
            self.ids.status18.color = (0, 0, 0, 1)
        else:
            self.ids.status18.text = "ABSENT"
            self.ids.status18.color = (1, 1, 1, 1)
        if absentInfo[18][1] == "present":
            self.ids.status19.text = "PRESENT"
            self.ids.status19.color = (0, 0, 0, 1)
        else:
            self.ids.status19.text = "ABSENT"
            self.ids.status19.color = (1, 1, 1, 1)
        if absentInfo[19][1] == "present":
            self.ids.status20.text = "PRESENT"
            self.ids.status20.color = (0, 0, 0, 1)
        else:
            self.ids.status20.text = "ABSENT"
            self.ids.status20.color = (1, 1, 1, 1)
        if absentInfo[20][1] == "present":
            self.ids.status21.text = "PRESENT"
            self.ids.status21.color = (0, 0, 0, 1)
        else:
            self.ids.status21.text = "ABSENT"
            self.ids.status21.color = (1, 1, 1, 1)
        if absentInfo[21][1] == "present":
            self.ids.status22.text = "PRESENT"
            self.ids.status22.color = (0, 0, 0, 1)
        else:
            self.ids.status22.text = "ABSENT"
            self.ids.status22.color = (1, 1, 1, 1)
        if absentInfo[22][1] == "present":
            self.ids.status23.text = "PRESENT"
            self.ids.status23.color = (0, 0, 0, 1)
        else:
            self.ids.status23.text = "ABSENT"
            self.ids.status23.color = (1, 1, 1, 1)
        if absentInfo[23][1] == "present":
            self.ids.status24.text = "PRESENT"
            self.ids.status24.color = (0, 0, 0, 1)
        else:
            self.ids.status24.text = "ABSENT"
            self.ids.status24.color = (1, 1, 1, 1)
        if absentInfo[24][1] == "present":
            self.ids.status25.text = "PRESENT"
            self.ids.status25.color = (0, 0, 0, 1)
        else:
            self.ids.status25.text = "ABSENT"
            self.ids.status25.color = (1, 1, 1, 1)
        if absentInfo[25][1] == "present":
            self.ids.status26.text = "PRESENT"
            self.ids.status26.color = (0, 0, 0, 1)
        else:
            self.ids.status26.text = "ABSENT"
            self.ids.status26.color = (1, 1, 1, 1)
        if absentInfo[26][1] == "present":
            self.ids.status27.text = "PRESENT"
            self.ids.status27.color = (0, 0, 0, 1)
        else:
            self.ids.status27.text = "ABSENT"
            self.ids.status27.color = (1, 1, 1, 1)
        if absentInfo[27][1] == "present":
            self.ids.status28.text = "PRESENT"
            self.ids.status28.color = (0, 0, 0, 1)
        else:
            self.ids.status28.text = "ABSENT"
            self.ids.status28.color = (1, 1, 1, 1)
        if absentInfo[28][1] == "present":
            self.ids.status29.text = "PRESENT"
            self.ids.status29.color = (0, 0, 0, 1)
        else:
            self.ids.status29.text = "ABSENT"
            self.ids.status29.color = (1, 1, 1, 1)
        if absentInfo[29][1] == "present":
            self.ids.status30.text = "PRESENT"
            self.ids.status30.color = (0, 0, 0, 1)
        else:
            self.ids.status30.text = "ABSENT"
            self.ids.status30.color = (1, 1, 1, 1)

    def selectAsVisited(self, room):
        if room == 1:
            if 0.30 < self.ids.visited1.background_color[0] < 0.31:
                self.ids.visited1.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited1.color = (0, 0, 0, 1)
            else:
                self.ids.visited1.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited1.color = (1, 1, 1, 1)
        if room == 2:
            if 0.30 < self.ids.visited2.background_color[0] < 0.31:
                self.ids.visited2.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited2.color = (0, 0, 0, 1)
            else:
                self.ids.visited2.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited2.color = (1, 1, 1, 1)
        if room == 3:
            if 0.30 < self.ids.visited3.background_color[0] < 0.31:
                self.ids.visited3.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited3.color = (0, 0, 0, 1)
            else:
                self.ids.visited3.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited3.color = (1, 1, 1, 1)
        if room == 4:
            if 0.30 < self.ids.visited4.background_color[0] < 0.31:
                self.ids.visited4.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited4.color = (0, 0, 0, 1)
            else:
                self.ids.visited4.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited4.color = (1, 1, 1, 1)
        if room == 5:
            if 0.30 < self.ids.visited5.background_color[0] < 0.31:
                self.ids.visited5.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited5.color = (0, 0, 0, 1)
            else:
                self.ids.visited5.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited5.color = (1, 1, 1, 1)
        if room == 6:
            if 0.30 < self.ids.visited6.background_color[0] < 0.31:
                self.ids.visited6.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited6.color = (0, 0, 0, 1)
            else:
                self.ids.visited6.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited6.color = (1, 1, 1, 1)
        if room == 7:
            if 0.30 < self.ids.visited7.background_color[0] < 0.31:
                self.ids.visited7.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited7.color = (0, 0, 0, 1)
            else:
                self.ids.visited7.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited7.color = (1, 1, 1, 1)
        if room == 8:
            if 0.30 < self.ids.visited8.background_color[0] < 0.31:
                self.ids.visited8.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited8.color = (0, 0, 0, 1)
            else:
                self.ids.visited8.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited8.color = (1, 1, 1, 1)
        if room == 9:
            if 0.30 < self.ids.visited9.background_color[0] < 0.31:
                self.ids.visited9.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited9.color = (0, 0, 0, 1)
            else:
                self.ids.visited9.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited9.color = (1, 1, 1, 1)
        if room == 10:
            if 0.30 < self.ids.visited10.background_color[0] < 0.31:
                self.ids.visited10.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited10.color = (0, 0, 0, 1)
            else:
                self.ids.visited10.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited10.color = (1, 1, 1, 1)
        if room == 11:
            if 0.30 < self.ids.visited11.background_color[0] < 0.31:
                self.ids.visited11.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited11.color = (0, 0, 0, 1)
            else:
                self.ids.visited11.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited11.color = (1, 1, 1, 1)
        if room == 12:
            if 0.30 < self.ids.visited12.background_color[0] < 0.31:
                self.ids.visited12.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited12.color = (0, 0, 0, 1)
            else:
                self.ids.visited12.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited12.color = (1, 1, 1, 1)
        if room == 13:
            if 0.30 < self.ids.visited13.background_color[0] < 0.31:
                self.ids.visited13.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited13.color = (0, 0, 0, 1)
            else:
                self.ids.visited13.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited13.color = (1, 1, 1, 1)
        if room == 14:
            if 0.30 < self.ids.visited14.background_color[0] < 0.31:
                self.ids.visited14.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited14.color = (0, 0, 0, 1)
            else:
                self.ids.visited14.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited14.color = (1, 1, 1, 1)
        if room == 15:
            if 0.30 < self.ids.visited15.background_color[0] < 0.31:
                self.ids.visited15.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited15.color = (0, 0, 0, 1)
            else:
                self.ids.visited15.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited15.color = (1, 1, 1, 1)
        if room == 16:
            if 0.30 < self.ids.visited16.background_color[0] < 0.31:
                self.ids.visited16.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited16.color = (0, 0, 0, 1)
            else:
                self.ids.visited16.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited16.color = (1, 1, 1, 1)
        if room == 17:
            if 0.30 < self.ids.visited17.background_color[0] < 0.31:
                self.ids.visited17.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited17.color = (0, 0, 0, 1)
            else:
                self.ids.visited17.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited17.color = (1, 1, 1, 1)
        if room == 18:
            if 0.30 < self.ids.visited18.background_color[0] < 0.31:
                self.ids.visited18.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited18.color = (0, 0, 0, 1)
            else:
                self.ids.visited18.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited18.color = (1, 1, 1, 1)
        if room == 19:
            if 0.30 < self.ids.visited19.background_color[0] < 0.31:
                self.ids.visited19.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited19.color = (0, 0, 0, 1)
            else:
                self.ids.visited19.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited19.color = (1, 1, 1, 1)
        if room == 20:
            if 0.30 < self.ids.visited20.background_color[0] < 0.31:
                self.ids.visited20.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited20.color = (0, 0, 0, 1)
            else:
                self.ids.visited20.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited20.color = (1, 1, 1, 1)
        if room == 21:
            if 0.30 < self.ids.visited21.background_color[0] < 0.31:
                self.ids.visited21.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited21.color = (0, 0, 0, 1)
            else:
                self.ids.visited21.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited21.color = (1, 1, 1, 1)
        if room == 22:
            if 0.30 < self.ids.visited22.background_color[0] < 0.31:
                self.ids.visited22.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited22.color = (0, 0, 0, 1)
            else:
                self.ids.visited22.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited22.color = (1, 1, 1, 1)
        if room == 23:
            if 0.30 < self.ids.visited23.background_color[0] < 0.31:
                self.ids.visited23.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited23.color = (0, 0, 0, 1)
            else:
                self.ids.visited23.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited23.color = (1, 1, 1, 1)
        if room == 24:
            if 0.30 < self.ids.visited24.background_color[0] < 0.31:
                self.ids.visited24.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited24.color = (0, 0, 0, 1)
            else:
                self.ids.visited24.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited24.color = (1, 1, 1, 1)
        if room == 25:
            if 0.30 < self.ids.visited25.background_color[0] < 0.31:
                self.ids.visited25.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited25.color = (0, 0, 0, 1)
            else:
                self.ids.visited25.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited25.color = (1, 1, 1, 1)
        if room == 26:
            if 0.30 < self.ids.visited26.background_color[0] < 0.31:
                self.ids.visited26.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited26.color = (0, 0, 0, 1)
            else:
                self.ids.visited26.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited26.color = (1, 1, 1, 1)
        if room == 27:
            if 0.30 < self.ids.visited27.background_color[0] < 0.31:
                self.ids.visited27.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited27.color = (0, 0, 0, 1)
            else:
                self.ids.visited27.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited27.color = (1, 1, 1, 1)
        if room == 28:
            if 0.30 < self.ids.visited28.background_color[0] < 0.31:
                self.ids.visited28.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited28.color = (0, 0, 0, 1)
            else:
                self.ids.visited28.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited28.color = (1, 1, 1, 1)
        if room == 29:
            if 0.30 < self.ids.visited29.background_color[0] < 0.31:
                self.ids.visited29.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited29.color = (0, 0, 0, 1)
            else:
                self.ids.visited29.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited29.color = (1, 1, 1, 1)
        if room == 30:
            if 0.30 < self.ids.visited30.background_color[0] < 0.31:
                self.ids.visited30.background_color = (0 / 255, 224 / 255, 161 / 255, 1)
                self.ids.visited30.color = (0, 0, 0, 1)
            else:
                self.ids.visited30.background_color = (78 / 255, 128 / 255, 152 / 255, 1)
                self.ids.visited30.color = (1, 1, 1, 1)


class KitchenWindow(Screen):
    pass


class IngredientsWindow(Screen):
    # noinspection PyMethodMayBeStatic
    def parseDataDiet(self):

        today = date.today()
        penultimateMonday = today - timedelta(days=today.weekday(), weeks=1)
        lastMonday = today - timedelta(days=today.weekday())
        comingMonday = today + timedelta(days=-today.weekday(), weeks=1)
        nextNextMonday = today + timedelta(days=-today.weekday(), weeks=2)

        nextNextMonday = str(nextNextMonday).replace("-", "")
        lastMonday = str(lastMonday).replace("-", "")
        comingMonday = str(comingMonday).replace("-", "")

        return lastMonday, comingMonday, penultimateMonday, nextNextMonday

    def checkAmounts(self):
        dietsClassicThisWeek = 0
        dietsClassicNextWeek = 0
        dietsVegetarianThisWeek = 0
        dietsVegetarianNextWeek = 0
        dietsVeganThisWeek = 0
        dietsVeganNextWeek = 0
        lastMonday, comingMonday, penultimateMonday, nextNextMonday = self.parseDataDiet()
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()

        cur.execute("SELECT classic, vegetarian, vegan, startdate, enddate FROM diets")
        diets = cur.fetchall()

        for diet in diets:
            if int(diet[4]) >= int(lastMonday):
                if int(diet[4]) < int(comingMonday) and int(diet[3]) <= int(lastMonday):
                    lDate = date(int(str(diet[4])[:4]), int(str(diet[4])[4:6]), int(str(diet[4])[6:]))
                    fDate = date(int(lastMonday[:4]), int(lastMonday[4:6]), int(lastMonday[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days + 1
                elif int(diet[4]) < int(comingMonday) and int(diet[3]) > int(lastMonday):
                    lDate = date(int(str(diet[4])[:4]), int(str(diet[4])[4:6]), int(str(diet[4])[6:]))
                    fDate = date(int(str(diet[3])[:4]), int(str(diet[3])[4:6]), int(str(diet[3])[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days + 1
                elif int(diet[4]) >= int(comingMonday) and int(diet[3]) > int(lastMonday):
                    lDate = date(int(comingMonday[:4]), int(comingMonday[4:6]), int(comingMonday[6:]))
                    fDate = date(int(str(diet[3])[:4]), int(str(diet[3])[4:6]), int(str(diet[3])[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days
                elif int(diet[4]) >= int(comingMonday) and int(diet[3]) > int(lastMonday):
                    multiply = 7
                else:
                    multiply = 0

                dietsClassicThisWeek = dietsClassicThisWeek + (int(diet[0]) * multiply)
                dietsVegetarianThisWeek = dietsVegetarianThisWeek + (int(diet[1]) * multiply)
                dietsVeganThisWeek = dietsVeganThisWeek + (int(diet[2]) * multiply)

        self.ids.classicThisWeek.text = str(dietsClassicThisWeek)
        self.ids.vegetarianThisWeek.text = str(dietsVegetarianThisWeek)
        self.ids.veganThisWeek.text = str(dietsVeganThisWeek)

        for diet in diets:
            if int(diet[4]) >= int(comingMonday):
                if int(diet[4]) < int(nextNextMonday) and int(diet[3]) <= int(
                        comingMonday):  # before end and before start
                    lDate = date(int(str(diet[4])[:4]), int(str(diet[4])[4:6]), int(str(diet[4])[6:]))
                    fDate = date(int(comingMonday[:4]), int(comingMonday[4:6]), int(comingMonday[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days + 1
                elif int(diet[4]) < int(nextNextMonday) and int(diet[3]) > int(
                        comingMonday):  # before end and after start
                    lDate = date(int(str(diet[4])[:4]), int(str(diet[4])[4:6]), int(str(diet[4])[6:]))
                    fDate = date(int(str(diet[3])[:4]), int(str(diet[3])[4:6]), int(str(diet[3])[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days + 1
                elif int(diet[4]) >= int(nextNextMonday) and int(diet[3]) > int(
                        comingMonday):
                    lDate = date(int(nextNextMonday[:4]), int(nextNextMonday[4:6]), int(nextNextMonday[6:]))
                    fDate = date(int(str(diet[3])[:4]), int(str(diet[3])[4:6]), int(str(diet[3])[6:]))
                    multiply = lDate - fDate
                    multiply = multiply.days
                elif int(diet[4]) >= int(nextNextMonday) and int(diet[3]) > int(
                        comingMonday):
                    multiply = 7
                else:
                    multiply = 0

                dietsClassicNextWeek = dietsClassicNextWeek + (int(diet[0]) * multiply)
                dietsVegetarianNextWeek = dietsVegetarianNextWeek + (int(diet[1]) * multiply)
                dietsVeganNextWeek = dietsVeganNextWeek + (int(diet[2]) * multiply)

        self.ids.classicNextWeek.text = str(dietsClassicNextWeek)
        self.ids.vegetarianNextWeek.text = str(dietsVegetarianNextWeek)
        self.ids.veganNextWeek.text = str(dietsVeganNextWeek)
        conn.commit()

        cur.close()

        conn.close()


class DailyKitchenWindow(Screen):
    # noinspection PyMethodMayBeStatic
    def parseDataDiet(self):
        currentYear = str(datetime.now().year)
        currentMonth = str(datetime.now().month)
        currentDay = str(datetime.now().day)
        if int(currentMonth) < 10:
            startMonthToDatabase = str(0) + str(currentMonth)
        else:
            startMonthToDatabase = str(currentMonth)
        if int(currentDay) < 10:
            startDayToDatabase = str(0) + str(currentDay)
        else:
            startDayToDatabase = str(currentDay)

        dateToDietToday = str(currentYear) + str(startMonthToDatabase) + str(startDayToDatabase)
        dateToDietTomorrow = date.today() + timedelta(days=1)
        dateToDietTomorrow = str(dateToDietTomorrow).replace("-", "")
        return dateToDietToday, dateToDietTomorrow

    def checkAmounts(self):
        dietsClassicToday = 0
        dietsClassicTomorrow = 0
        dietsVegetarianToday = 0
        dietsVegetarianTomorrow = 0
        dietsVeganToday = 0
        dietsVeganTomorrow = 0
        dateToDietToday, dateToDietTomorrow = self.parseDataDiet()
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        cur.execute("SELECT classic, vegetarian, vegan, startdate, enddate FROM diets WHERE startdate<='" + str(
            dateToDietToday) + "' AND enddate>='" + str(dateToDietToday) + "'")
        dietsToday = cur.fetchall()
        cur.execute("SELECT classic, vegetarian, vegan, startdate, enddate FROM diets WHERE startdate<='" + str(
            dateToDietTomorrow) + "' AND enddate>'" + str(dateToDietTomorrow) + "'")
        dietsTomorrow = cur.fetchall()

        for diet in dietsToday:
            dietsClassicToday = dietsClassicToday + int(diet[0])
            dietsVegetarianToday = dietsVegetarianToday + int(diet[1])
            dietsVeganToday = dietsVeganToday + int(diet[2])

        for diet in dietsTomorrow:
            dietsClassicTomorrow = dietsClassicTomorrow + int(diet[0])
            dietsVegetarianTomorrow = dietsVegetarianTomorrow + int(diet[1])
            dietsVeganTomorrow = dietsVeganTomorrow + int(diet[2])

        self.ids.classicToday.text = str(dietsClassicToday)
        self.ids.vegetarianToday.text = str(dietsVegetarianToday)
        self.ids.veganToday.text = str(dietsVeganToday)

        self.ids.classicTomorrow.text = str(dietsClassicTomorrow)
        self.ids.vegetarianTomorrow.text = str(dietsVegetarianTomorrow)
        self.ids.veganTomorrow.text = str(dietsVeganTomorrow)
        conn.commit()

        cur.close()

        conn.close()

    def lowerAmount(self, button, resetFlag):
        if resetFlag == 1:
            self.ids.classicToday.text = str(0)
            self.ids.vegetarianToday.text = str(0)
            self.ids.veganToday.text = str(0)
        else:
            if button == "classicToday" and int(self.ids.classicToday.text) != 0:
                self.ids.classicToday.text = str(int(self.ids.classicToday.text) - 1)
            if button == "vegetarianToday" and int(self.ids.vegetarianToday.text) != 0:
                self.ids.vegetarianToday.text = str(int(self.ids.vegetarianToday.text) - 1)
            if button == "veganToday" and int(self.ids.veganToday.text) != 0:
                self.ids.veganToday.text = str(int(self.ids.veganToday.text) - 1)

            if button == "classicTomorrow" and int(self.ids.classicTomorrow.text) != 0:
                self.ids.classicTomorrow.text = str(int(self.ids.classicTomorrow.text) - 1)
            if button == "vegetarianTomorrow" and int(self.ids.vegetarianTomorrow.text) != 0:
                self.ids.vegetarianTomorrow.text = str(int(self.ids.vegetarianTomorrow.text) - 1)
            if button == "veganTomorrow" and int(self.ids.veganTomorrow.text) != 0:
                self.ids.veganTomorrow.text = str(int(self.ids.veganTomorrow.text) - 1)


class DateWindow(Screen):
    # noinspection PyMethodMayBeStatic
    def abortUpdate(self):
        if len(HotelManager.roomInfo) > 0 and len(HotelManager.clientInfo) > 0:
            conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

            cur = conn.cursor()
            cur.execute("INSERT INTO room" + str(HotelManager.roomInfo[0][
                                                     0]) + " (roomnumber, startdate, enddate, clientid) VALUES (" + str(
                HotelManager.roomInfo[0][0]) + ", '" + str(
                HotelManager.roomInfo[0][1]) + "', '" + str(
                HotelManager.roomInfo[0][2]) + "', " + str(
                HotelManager.roomInfo[0][3]) + ")")
            conn.commit()
            cur.execute("INSERT INTO clients (firstname, lastname, email, telephone, clientid) VALUES ('" + str(
                HotelManager.clientInfo[0][0]) + "', '" + str(
                HotelManager.clientInfo[0][1]) + "', '" + str(
                HotelManager.clientInfo[0][2]) + "', '" + str(
                HotelManager.clientInfo[0][3]) + "', " + str(
                HotelManager.clientInfo[0][4]) + ")")

            conn.commit()

            cur.close()

            conn.close()
            HotelManager.roomInfo = []
            HotelManager.clientInfo = []
            return "browserWindow"
        else:
            return "actionWindow"

    # noinspection PyMethodMayBeStatic
    def startUpdate(self):
        if len(HotelManager.bookToUpdate) > 0:
            conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM room" + str(HotelManager.bookToUpdate[0]) + " WHERE startdate='" + str(
                    HotelManager.bookToUpdate[3]) + "' AND enddate='" + str(
                    HotelManager.bookToUpdate[4] + "'"))
            HotelManager.roomInfo = cur.fetchall()
            cur.execute("SELECT * FROM clients WHERE lastname='" + str(
                HotelManager.bookToUpdate[1]) + "' AND email='" + str(
                HotelManager.bookToUpdate[2] + "'"))
            HotelManager.clientInfo = cur.fetchall()
            cur.execute(
                "DELETE FROM room" + str(HotelManager.bookToUpdate[0]) + " WHERE startdate='" + str(
                    HotelManager.bookToUpdate[3]) + "' AND enddate='" + str(
                    HotelManager.bookToUpdate[4] + "'"))
            conn.commit()
            cur.execute("DELETE FROM clients WHERE lastname='" + str(
                HotelManager.bookToUpdate[1]) + "' AND email='" + str(
                HotelManager.bookToUpdate[2] + "'"))
            conn.commit()

            cur.close()

            conn.close()

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

        HotelManager.startDayOutput = ""
        HotelManager.endDayOutput = ""
        HotelManager.startMonthOutput = ""
        HotelManager.endMonthOutput = ""
        HotelManager.startYearOutput = ""
        HotelManager.endYearOutput = ""
        HotelManager.selectedRoomNumbers = []
        HotelManager.clientInformation = []
        HotelManager.startDateToCheckColor = ""
        HotelManager.endDateToCheckColor = ""

        return self.abortUpdate()

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
        HotelManager.startDayOutput = self.ids.startDay.text
        HotelManager.startMonthOutput = self.ids.startMonth.text
        HotelManager.startYearOutput = self.ids.startYear.text
        HotelManager.endDayOutput = self.ids.endDay.text
        HotelManager.endMonthOutput = self.ids.endMonth.text
        HotelManager.endYearOutput = self.ids.endYear.text
        HotelManager.startDateToCheckColor, HotelManager.endDateToCheckColor = \
            dataParsing()
        return 'roomWindow'


def turnRedIfUnavailable():
    startDate = HotelManager.startDateToCheckColor
    endDate = HotelManager.endDateToCheckColor

    conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

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

    cur.close()

    conn.close()
    return unavailableRooms


def dataParsing():
    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
              "NOVEMBER", "DECEMBER"]
    if int(months.index(HotelManager.startMonthOutput) + 1) < 10:
        startMonthToDatabase = str(0) + str(
            int(months.index(HotelManager.startMonthOutput) + 1))
    else:
        startMonthToDatabase = str(int(months.index(HotelManager.startMonthOutput) + 1))
    if int(HotelManager.startDayOutput) < 10:
        startDayToDatabase = str(0) + str(int(HotelManager.startDayOutput))
    else:
        startDayToDatabase = str(int(HotelManager.startDayOutput))

    if int(months.index(HotelManager.endMonthOutput) + 1) < 10:
        endMonthToDatabase = str(0) + str(
            int(months.index(HotelManager.endMonthOutput) + 1))
    else:
        endMonthToDatabase = str(int(months.index(HotelManager.endMonthOutput)) + 1)
    if int(HotelManager.endDayOutput) < 10:
        endDayToDatabase = str(0) + str(int(HotelManager.endDayOutput))
    else:
        endDayToDatabase = str(int(HotelManager.endDayOutput))
    startDateToCheckColor = str(
        HotelManager.startYearOutput) + startMonthToDatabase + startDayToDatabase
    endDateToCheckColor = str(HotelManager.endYearOutput) + endMonthToDatabase + endDayToDatabase
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
            if room in HotelManager.selectedRoomNumbers:
                HotelManager.selectedRoomNumbers.remove(room)
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
        if self.ids.room1.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(1)
            self.ids.room1.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room1.background_color[0] < 0.57:  # if blue
            self.ids.room1.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(1)

    def selectedRoom2(self):
        if self.ids.room2.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(2)
            self.ids.room2.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room2.background_color[0] < 0.57:
            self.ids.room2.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(2)

    def selectedRoom3(self):
        if self.ids.room3.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(3)
            self.ids.room3.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room3.background_color[0] < 0.57:
            self.ids.room3.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(3)

    def selectedRoom4(self):
        if self.ids.room4.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(4)
            self.ids.room4.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room4.background_color[0] < 0.57:
            self.ids.room4.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(4)

    def selectedRoom5(self):
        if self.ids.room5.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(5)
            self.ids.room5.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room5.background_color[0] < 0.57:
            self.ids.room5.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(5)

    def selectedRoom6(self):
        if self.ids.room6.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(6)
            self.ids.room6.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room6.background_color[0] < 0.57:
            self.ids.room6.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(6)

    def selectedRoom7(self):
        if self.ids.room7.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(7)
            self.ids.room7.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room7.background_color[0] < 0.57:
            self.ids.room7.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(7)

    def selectedRoom8(self):
        if self.ids.room8.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(8)
            self.ids.room8.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room8.background_color[0] < 0.57:
            self.ids.room8.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(8)

    def selectedRoom9(self):
        if self.ids.room9.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(9)
            self.ids.room9.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room9.background_color[0] < 0.57:
            self.ids.room9.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(9)

    def selectedRoom10(self):
        if self.ids.room10.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(10)
            self.ids.room10.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room10.background_color[0] < 0.57:
            self.ids.room10.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(10)

    def selectedRoom11(self):
        if self.ids.room11.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(11)
            self.ids.room11.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room11.background_color[0] < 0.57:
            self.ids.room11.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(11)

    def selectedRoom12(self):
        if self.ids.room12.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(12)
            self.ids.room12.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room12.background_color[0] < 0.57:
            self.ids.room12.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(12)

    def selectedRoom13(self):
        if self.ids.room13.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(13)
            self.ids.room13.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room13.background_color[0] < 0.57:
            self.ids.room13.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(13)

    def selectedRoom14(self):
        if self.ids.room14.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(14)
            self.ids.room14.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room14.background_color[0] < 0.57:
            self.ids.room14.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(14)

    def selectedRoom15(self):
        if self.ids.room15.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(15)
            self.ids.room15.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room15.background_color[0] < 0.57:
            self.ids.room15.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(15)

    def selectedRoom16(self):
        if self.ids.room16.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(16)
            self.ids.room16.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room16.background_color[0] < 0.57:
            self.ids.room16.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(16)

    def selectedRoom17(self):
        if self.ids.room17.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(17)
            self.ids.room17.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room17.background_color[0] < 0.57:
            self.ids.room17.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(17)

    def selectedRoom18(self):
        if self.ids.room18.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(18)
            self.ids.room18.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room18.background_color[0] < 0.57:
            self.ids.room18.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(18)

    def selectedRoom19(self):
        if self.ids.room19.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(19)
            self.ids.room19.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room19.background_color[0] < 0.57:
            self.ids.room19.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(19)

    def selectedRoom20(self):
        if self.ids.room20.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(20)
            self.ids.room20.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room20.background_color[0] < 0.57:
            self.ids.room20.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(20)


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
            if room in HotelManager.selectedRoomNumbers:
                HotelManager.selectedRoomNumbers.remove(room)
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
        if self.ids.room21.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(21)
            self.ids.room21.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room21.background_color[0] < 0.57:
            self.ids.room21.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(21)

    def selectedRoom22(self):
        if self.ids.room22.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(22)
            self.ids.room22.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room22.background_color[0] < 0.57:
            self.ids.room22.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(22)

    def selectedRoom23(self):
        if self.ids.room23.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(23)
            self.ids.room23.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room23.background_color[0] < 0.57:
            self.ids.room23.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(23)

    def selectedRoom24(self):
        if self.ids.room24.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(24)
            self.ids.room24.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room24.background_color[0] < 0.57:
            self.ids.room24.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(24)

    def selectedRoom25(self):
        if self.ids.room25.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(25)
            self.ids.room25.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room25.background_color[0] < 0.57:
            self.ids.room25.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(25)

    def selectedRoom26(self):
        if self.ids.room26.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(26)
            self.ids.room26.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room26.background_color[0] < 0.57:
            self.ids.room6.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(26)

    def selectedRoom27(self):
        if self.ids.room27.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(27)
            self.ids.room27.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room27.background_color[0] < 0.57:
            self.ids.room27.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(27)

    def selectedRoom28(self):
        if self.ids.room28.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(28)
            self.ids.room28.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room28.background_color[0] < 0.57:
            self.ids.room28.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(28)

    def selectedRoom29(self):
        if self.ids.room29.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(29)
            self.ids.room29.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room29.background_color[0] < 0.57:
            self.ids.room29.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(29)

    def selectedRoom30(self):
        if self.ids.room30.background_color[0] == 0:
            HotelManager.selectedRoomNumbers.remove(30)
            self.ids.room30.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
        elif 0.55 < self.ids.room30.background_color[0] < 0.57:
            self.ids.room30.background_color = (0, 224 / 255, 161 / 255, 1)
            HotelManager.selectedRoomNumbers.append(30)


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

        HotelManager.startDayOutput = ""
        HotelManager.endDayOutput = ""
        HotelManager.startMonthOutput = ""
        HotelManager.endMonthOutput = ""
        HotelManager.startYearOutput = ""
        HotelManager.endYearOutput = ""
        HotelManager.selectedRoomNumbers = []
        HotelManager.clientInformation = []
        HotelManager.startDateToCheckColor = ""
        HotelManager.endDateToCheckColor = ""

    def registerPress(self):  # TODO no the same e-mails and telephone numbers
        if isRightName(self.ids.firstName.text) and isRightName(self.ids.lastName.text) and isRightEmail(
                self.ids.email.text) and isRightTelephoneNumber(self.ids.telephone.text):
            HotelManager.clientInformation.append(self.ids.firstName.text)
            HotelManager.clientInformation.append(self.ids.lastName.text)
            HotelManager.clientInformation.append(self.ids.email.text)
            HotelManager.clientInformation.append(self.ids.telephone.text)

            conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

            cur = conn.cursor()
            cur.execute("SELECT MAX(clientID) FROM clients")
            maxID = cur.fetchall()[0][0]
            if maxID is None:
                maxID = 1
            else:
                maxID = int(maxID) + 1
            cur.execute("SELECT clientID FROM clients WHERE email = '" + HotelManager.clientInformation[
                2] + "' AND telephone = '" + HotelManager.clientInformation[3] + "'")
            existedClientID = cur.fetchall()
            if len(existedClientID):
                selectedID = existedClientID[0][0]
            else:
                selectedID = maxID
                cur.execute(
                    "INSERT INTO clients VALUES('" + HotelManager.clientInformation[0] + "', '" +
                    HotelManager.clientInformation[1] + "', '" +
                    HotelManager.clientInformation[2] + "', '" +
                    HotelManager.clientInformation[3] + "', '" + str(selectedID) + "')")
                conn.commit()
            if int(self.months.index(HotelManager.startMonthOutput) + 1) < 10:
                startMonthToDatabase = str(0) + str(
                    int(self.months.index(HotelManager.startMonthOutput) + 1))
            else:
                startMonthToDatabase = str(int(self.months.index(HotelManager.startMonthOutput) + 1))
            if int(HotelManager.startDayOutput) < 10:
                startDayToDatabase = str(0) + str(int(HotelManager.startDayOutput))
            else:
                startDayToDatabase = str(int(HotelManager.startDayOutput))

            if int(self.months.index(HotelManager.endMonthOutput) + 1) < 10:
                endMonthToDatabase = str(0) + str(
                    int(self.months.index(HotelManager.endMonthOutput) + 1))
            else:
                endMonthToDatabase = str(int(self.months.index(HotelManager.endMonthOutput)) + 1)
            if int(HotelManager.endDayOutput) < 10:
                endDayToDatabase = str(0) + str(int(HotelManager.endDayOutput))
            else:
                endDayToDatabase = str(int(HotelManager.endDayOutput))

            for room in HotelManager.selectedRoomNumbers:
                cur.execute("INSERT INTO room" + str(room) + " VALUES('" + str(
                    room) + "', '" + HotelManager.startYearOutput + startMonthToDatabase +
                            startDayToDatabase + "', '" + HotelManager.endYearOutput +
                            endMonthToDatabase + endDayToDatabase + "', '" + str(selectedID) + "')")
            conn.commit()

            cur.close()

            conn.close()
            HotelManager.dateWindowStartDataFromLastBook = str(
                HotelManager.startYearOutput) + str(startMonthToDatabase) + str(startDayToDatabase)
            HotelManager.dateWindowEndDataFromLastBook = str(
                HotelManager.endYearOutput) + str(endMonthToDatabase) + str(endDayToDatabase)
            HotelManager.dateWindowEmailFromLastBook = str(self.ids.email.text)
            self.resetToDefaults()
            return True
        else:
            return False


class ScreenButton(Button):
    roomData = ObjectProperty(None)
    background_color = ObjectProperty(None)
    id = ObjectProperty(None)

    def on_press(self, *args):
        if 0.63 < self.background_color[0] < 0.64:
            self.background_color = (144 / 255, 194 / 255, 231 / 255, 1)
            self.color = (0, 0, 0, 1)
            HotelManager.amountToUpdate = HotelManager.amountToUpdate - 1
        else:
            self.background_color = (
                163 / 255, 22 / 255, 33 / 255, 1)  # TODO repair schedule so not last matched red is data
            self.color = (1, 1, 1, 1)
            HotelManager.bookToUpdate = self.roomData
            HotelManager.amountToUpdate = HotelManager.amountToUpdate + 1


class BrowserWindow(Screen):
    mainLayoutForKv = ObjectProperty(None)

    # noinspection PyMethodMayBeStatic
    def reloadScroll(self):
        self.ids.main.remove_widget(self.mainLayoutForKv)
        self.mainLayoutForKv.clear_widgets()
        self.ids.main.add_widget(self.createBooksRows())

    # noinspection PyMethodMayBeStatic
    def createBooksRows(self):
        inputText = self.textToSelect.text
        inputCategory = self.columnToSelect.text
        scrollRoot = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.75))
        mainLayout = GridLayout(cols=1)
        self.ids['scrollID'] = mainLayout
        layout = GridLayout(padding=30, cols=6, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        header = GridLayout(padding=[30, 0, 30, 0], cols=6, spacing=20)
        header.add_widget(Label(text="ROOM", color=(0, 0, 0, 1), size_hint_x=None, width=50))
        header.add_widget(Label(text="LAST NAME", color=(0, 0, 0, 1)))
        header.add_widget(Label(text="E-MAIL", color=(0, 0, 0, 1)))
        header.add_widget(Label(text="START DATE", color=(0, 0, 0, 1), size_hint_x=None, width=90))
        header.add_widget(Label(text="END DATE", color=(0, 0, 0, 1), size_hint_x=None, width=90))
        header.add_widget(Label(text="UPDATE", color=(0, 0, 0, 1), size_hint_x=None, width=60))

        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        dataToBrowse = []
        if len(inputText) == 0 or inputCategory == "CATEGORY":
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
        elif inputCategory == "ROOM":
            if 1 <= len(inputText) <= 2 and inputText[0].isdigit():
                cur.execute(
                    "SELECT room" + str(inputText) + ".roomnumber, clients.lastname, clients.email, room" + str(
                        inputText) + ".startdate, room" + str(
                        inputText) + ".enddate FROM clients JOIN room" + str(
                        inputText) + " ON clients.clientid = room" + str(
                        inputText) + ".clientid ORDER BY room" + str(inputText) + ".startdate, room" + str(
                        inputText) + ".clientid, room" + str(inputText) + ".enddate")
                dataN = cur.fetchall()
                if len(dataN) > 0:
                    dataToBrowse.append(dataN)
        elif inputCategory == "START DATE" or inputCategory == "END DATE":
            if inputCategory == "START DATE": inputCategory = "startdate"
            if inputCategory == "END DATE": inputCategory = "enddate"

            if inputText[4] == " " or inputText[4] == "-" or inputText[4] == "/":
                inputText = str(inputText[:4]) + str(inputText[5:7]) + str(inputText[8:])
                for roomNumber in range(30):
                    cur.execute(
                        "SELECT room" + str(
                            roomNumber + 1) + ".roomnumber, clients.lastname, clients.email, room" + str(
                            roomNumber + 1) + ".startdate, room" + str(
                            roomNumber + 1) + ".enddate FROM clients JOIN room" + str(
                            roomNumber + 1) + " ON clients.clientid = room" + str(
                            roomNumber + 1) + ".clientid WHERE " + str(inputCategory) + "='" + str(
                            inputText) + "' ORDER BY room" + str(roomNumber + 1) + ".startdate, room" + str(
                            roomNumber + 1) + ".clientid, room" + str(roomNumber + 1) + ".enddate")
                    dataN = cur.fetchall()
                    if len(dataN) > 0:
                        dataToBrowse.append(dataN)
            elif inputText[2] == " " or inputText[2] == "-" or inputText[2] == "/":
                inputText = str(inputText[6:] + str(inputText[3:5]) + str(inputText[:2]))
                for roomNumber in range(30):
                    cur.execute(
                        "SELECT room" + str(
                            roomNumber + 1) + ".roomnumber, clients.lastname, clients.email, room" + str(
                            roomNumber + 1) + ".startdate, room" + str(
                            roomNumber + 1) + ".enddate FROM clients JOIN room" + str(
                            roomNumber + 1) + " ON clients.clientid = room" + str(
                            roomNumber + 1) + ".clientid WHERE " + str(inputCategory) + "='" + str(
                            inputText) + "' ORDER BY room" + str(roomNumber + 1) + ".startdate, room" + str(
                            roomNumber + 1) + ".clientid, room" + str(roomNumber + 1) + ".enddate")
                    dataN = cur.fetchall()
                    if len(dataN) > 0:
                        dataToBrowse.append(dataN)
        else:
            if inputCategory == "LAST NAME": inputCategory = "lastname"
            if inputCategory == "E-MAIL": inputCategory = "email"
            for roomNumber in range(30):
                cur.execute(
                    "SELECT room" + str(roomNumber + 1) + ".roomnumber, clients.lastname, clients.email, room" + str(
                        roomNumber + 1) + ".startdate, room" + str(
                        roomNumber + 1) + ".enddate FROM clients JOIN room" + str(
                        roomNumber + 1) + " ON clients.clientid = room" + str(
                        roomNumber + 1) + ".clientid WHERE " + str(inputCategory) + "='" + str(
                        inputText) + "' ORDER BY room" + str(roomNumber + 1) + ".startdate, room" + str(
                        roomNumber + 1) + ".clientid, room" + str(roomNumber + 1) + ".enddate")
                dataN = cur.fetchall()
                if len(dataN) > 0:
                    dataToBrowse.append(dataN)

        conn.commit()

        cur.close()

        conn.close()

        idButton = 0
        for i in range(len(dataToBrowse)):
            oneRoomData = dataToBrowse[i]
            for j in oneRoomData:
                idButton = idButton + 1
                startDate = j[3][6:] + "-" + j[3][4:6] + "-" + j[3][:4]
                endDate = j[4][6:] + "-" + j[4][4:6] + "-" + j[4][:4]
                layout.add_widget(Label(text=str(j[0]), color=(0, 0, 0, 1), size_hint_x=None, width=50))
                layout.add_widget(Label(text=str(j[1]), color=(0, 0, 0, 1)))
                layout.add_widget(Label(text=str(j[2]), color=(0, 0, 0, 1)))
                layout.add_widget(Label(text=startDate, color=(0, 0, 0, 1), size_hint_x=None, width=90))
                layout.add_widget(Label(text=endDate, color=(0, 0, 0, 1), size_hint_x=None, width=90))
                layout.add_widget(ScreenButton(text="SELECT", color=(0, 0, 0, 1),
                                               background_color=(144 / 255, 194 / 255, 231 / 255, 1),
                                               size_hint_y=None, height=30, size_hint_x=None, width=60,
                                               roomData=j, id="roomBrowse" + str(idButton)))  # TODO

        scrollRoot.add_widget(layout)
        mainLayout.add_widget(header)
        if len(dataToBrowse) == 0:
            mainLayout.add_widget(
                Label(text="NO RESULTS OR INVALID INPUT DATA", color=(163 / 255, 22 / 255, 33 / 255, 1)))
        mainLayout.add_widget(scrollRoot)
        self.mainLayoutForKv = mainLayout

        HotelManager.renderBrowser = False
        return self.mainLayoutForKv

    # noinspection PyMethodMayBeStatic
    def deleteBook(self):
        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        cur.execute("DELETE FROM room" + str(HotelManager.bookToUpdate[0]) + " WHERE startdate='" + str(
            HotelManager.bookToUpdate[3]) + "' AND enddate='" + str(
            HotelManager.bookToUpdate[4] + "'"))
        conn.commit()
        cur.execute("DELETE FROM clients WHERE lastname='" + str(
            HotelManager.bookToUpdate[1]) + "' AND email='" + str(
            HotelManager.bookToUpdate[2] + "'"))
        conn.commit()
        cur.execute("DELETE FROM diets WHERE email='" + HotelManager.bookToUpdate[2] + "'")
        conn.commit()

        cur.close()

        conn.close()
        self.reloadScroll()


class DietWindow(Screen):
    startDay = ObjectProperty(None)
    endDay = ObjectProperty(None)
    startMonth = ObjectProperty(None)
    endMonth = ObjectProperty(None)
    startYear = ObjectProperty(None)
    endYear = ObjectProperty(None)
    emailFood = ObjectProperty(None)

    currentYear = str(datetime.now().year)
    currentMonth = str(datetime.now().month)
    currentDay = str(datetime.now().day)
    daysStart = []
    for i in range(monthrange(int(currentYear), int(currentMonth))[1]):
        daysStart.append(str(i + 1))
    daysEnd = daysStart.copy()

    # noinspection PyMethodMayBeStatic
    def startingValues(self):
        if len(HotelManager.dateWindowStartDataFromLastBook) > 0:
            lastStartDate = HotelManager.dateWindowStartDataFromLastBook
            lastEndDate = HotelManager.dateWindowEndDataFromLastBook
            self.ids.startYear.text = lastStartDate[:4]
            self.ids.startMonth.text = lastStartDate[4:6]
            self.ids.startDay.text = lastStartDate[6:]

            self.ids.endYear.text = lastEndDate[:4]
            self.ids.endMonth.text = lastEndDate[4:6]
            self.ids.endDay.text = lastEndDate[6:]

            self.ids.emailFood.text = HotelManager.dateWindowEmailFromLastBook

    def daysInSelectedMonthForStart(self):
        self.daysStart = []
        for i in range(monthrange(int(self.ids.startYear.text), int(self.ids.startMonth.text))[1]):
            self.daysStart.append(str(i + 1))
        self.startDay.values = self.daysStart
        if int(self.startDay.text) > int(self.daysStart[-1]):
            self.startDay.text = str(self.daysStart[-1])
        self.peopleLeft()

    def daysInSelectedMonthForEnd(self):
        self.daysEnd = []
        for i in range(monthrange(int(self.ids.endYear.text), int(self.ids.endMonth.text))[1]):
            self.daysEnd.append(str(i + 1))
        self.endDay.values = self.daysEnd
        if int(self.endDay.text) > int(self.daysEnd[-1]):
            self.endDay.text = str(self.daysEnd[-1])
        self.peopleLeft()

    def parseData(self):
        if int(self.ids.startMonth.text) < 10:
            startMonthToDatabase = str(0) + str(self.ids.startMonth.text)
        else:
            startMonthToDatabase = str(self.ids.startMonth.text)
        if int(self.ids.startDay.text) < 10:
            startDayToDatabase = str(0) + str(self.ids.startDay.text)
        else:
            startDayToDatabase = str(self.ids.startDay.text)

        if int(self.ids.endMonth.text) < 10:
            endMonthToDatabase = str(0) + str(self.ids.endMonth.text)
        else:
            endMonthToDatabase = str(self.ids.endMonth.text)
        if int(self.ids.endDay.text) < 10:
            endDayToDatabase = str(0) + str(self.ids.endDay.text)
        else:
            endDayToDatabase = str(self.ids.endDay.text)

        startingDate = str(self.ids.startYear.text) + str(startMonthToDatabase) + str(startDayToDatabase)
        endingDate = str(self.ids.endYear.text) + str(endMonthToDatabase) + str(endDayToDatabase)

        return startingDate, endingDate

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

    def limit_spinner(self):
        maxItems = 3
        self.spinner.dropdown_cls.max_height = maxItems * dp(48)
        self.peopleLeft()

    def peopleLeft(self):
        self.numberOfFood()
        answer = (self.multiplayer * 4) - int(self.ids.classicDiet.text) - int(self.ids.vegetarianDiet.text) - int(
            self.ids.veganDiet.text)
        peopleLeftValues = []
        for i in range(answer + 1):
            peopleLeftValues.append(str(i))
            self.ids.classicDiet.values = peopleLeftValues
            self.ids.vegetarianDiet.values = peopleLeftValues
            self.ids.veganDiet.values = peopleLeftValues

    multiplayer = 0

    def numberOfFood(self):

        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        dataToBrowse = []
        startingDate, endingDate = self.parseData()
        for roomNumber in range(30):
            cur.execute("SELECT clients.email, room" + str(roomNumber + 1) + ".startdate, room" + str(
                roomNumber + 1) + ".enddate FROM clients JOIN room" + str(
                roomNumber + 1) + " ON clients.clientid = room" + str(roomNumber + 1) + ".clientid WHERE room" + str(
                roomNumber + 1) + ".startdate='" + str(startingDate) + "' AND room" + str(
                roomNumber + 1) + ".enddate='" + str(endingDate) + "' AND clients.email='" + str(
                self.ids.emailFood.text) + "'")
            dataN = cur.fetchall()
            if len(dataN) > 0:
                dataToBrowse.append(dataN)
        conn.commit()

        cur.close()

        conn.close()
        self.multiplayer = len(dataToBrowse)

    # noinspection PyMethodMayBeStatic
    def saveFood(self):

        conn = psycopg2.connect(host="localhost", database="hotel", user="postgres", password="admin")

        cur = conn.cursor()
        if not isRightEmail(str(self.ids.emailFood.text)):
            return False
        if str(self.ids.classicDiet.text) == '0' and str(self.ids.vegetarianDiet.text) == '0' and str(
                self.ids.veganDiet.text) == '0':
            return False
        cur.execute("DELETE FROM diets WHERE email='" + str(self.ids.emailFood.text) + "' AND startdate='" + str(
            self.parseData()[0]) + "' AND enddate='" + str(self.parseData()[1]) + "'")
        conn.commit()
        cur.execute("INSERT INTO diets (email, startdate, enddate, classic, vegetarian, vegan) VALUES('" + str(
            self.ids.emailFood.text) + "', '" + str(self.parseData()[0]) + "', '" + str(
            self.parseData()[1]) + "', '" + str(self.ids.classicDiet.text) + "', '" + str(
            self.ids.vegetarianDiet.text) + "', '" + str(self.ids.veganDiet.text) + "')")
        conn.commit()

        cur.close()

        conn.close()
        return True


class WindowManager(ScreenManager):
    pass


# Name of style file
kv = Builder.load_file('design.kv')


class HotelManager(App):
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
    bookToUpdate = []
    renderBrowser = True
    clientInfo = []
    roomInfo = []
    amountToUpdate = 0
    dateWindowStartDataFromLastBook = ""
    dateWindowEndDataFromLastBook = ""
    dateWindowEmailFromLastBook = ""

    def build(self):
        Window.clearcolor = (206 / 255, 211 / 255, 220 / 255, 1)
        return kv


if __name__ == '__main__':
    HotelManager().run()
