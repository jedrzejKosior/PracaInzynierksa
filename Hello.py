from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

# Name of style file
Builder.load_file('main_page.kv')


class MyLayout(Widget):

    firstName = ObjectProperty(None)
    lastName = ObjectProperty(None)

    def press(self):
        firstName = self.firstName.text
        lastName = self.lastName.text
        # self.add_widget(Label(text=f"Hello {firstName}, {lastName}"))
        print(f"Hello {firstName}, {lastName}")
        # update button label
        self.ids.printName.text = f'Hello {firstName}!'
        # Clear input
        self.firstName.text = ""
        self.lastName.text = ""


class Application(App):
    def build(self):
        # background color
        Window.clearcolor = (206/255, 211/255, 220/255, 1)
        return MyLayout()


if __name__ == '__main__':
    Application().run()
