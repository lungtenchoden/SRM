from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HelloApp(App):
    def build(self):
        self.title = "Kivy Hello - Lungten Choden (14)"
        root = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.label = Label(text="Hello")
        button = Button(text="Click me")
        button.bind(on_press=self.on_click)
        root.add_widget(self.label)
        root.add_widget(button)
        return root

    def on_click(self, instance):
        self.label.text = "Hello, button clicked!"


HelloApp().run()