# from kivy.app import App
# from kivy.uix.label import Label

# class MyApp(App):
#     def build(self):
#         return Label(text="Hello, Kivy!")

# if __name__ == "__main__":
#     MyApp().run()
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen , FadeTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.uix.gridlayout import GridLayout
from quiz import QUIZ_DATA
from kivy.app import App
import random



LabelBase.register(name="ComicNeue", fn_regular="ComicNeue-Bold.ttf")


Config.set('kivy', 'default_font', ['ComicNeue-Bold'])


def blink_button(self, button, color1, color2, times=4, interval=0.2):
    def toggle_color(dt):
        nonlocal times
        if times > 0:
            button.background_color = color1 if times % 2 == 0 else color2
            times -= 1
            Clock.schedule_once(toggle_color, interval)
        else:
            button.background_color = color1
    toggle_color(0)

# for tribe_group_selection

class BackgroundBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 0.3)  # White overlay with 30% opacity
            self.bg = Rectangle(source="OdishaTribes.jpg", pos=self.pos, size=self.size)

        # Update background size with layout resize
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
         self.bg.size = self.size
         self.bg.pos = self.pos
         



class TribeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(source="cover_page.jpg", size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        title = Label(text="Welcome, Pick Your Tribe!",
                       font_size=36, 
                       color=(1, 1, 1, 1),
                       font_name="ComicNeue-Bold.ttf",
                       bold=True
                       )
        layout.add_widget(title)

        self.name_input = TextInput(
            hint_text="Enter your name",
            size_hint=(1, 0.15),
            multiline=False,
            font_name="ComicNeue-Bold.ttf",
            font_size=22,
            foreground_color=(0, 0, 0, 1),  # Black text
            background_color=(1, 1, 1, 0.7)  # White with transparency
        )
        layout.add_widget(self.name_input)
        tribes = ["Santali", "Ho", "Kui", "Munda"]
        colors = [
                (0.2, 0.6, 0.9, 1),   # Sky Blue
                (0.9, 0.5, 0.2, 1),   # Orange
                (0.3, 0.8, 0.4, 1),   # Green
                (0.7, 0.4, 0.9, 1)    # Purple
            ]

        for i, tribe in enumerate(tribes):
            btn = Button(
            text=tribe,
            size_hint=(1, 0.3),
            font_name="ComicNeue-Bold.ttf",
            font_size=24,
            background_color=colors[i]  # Different color for each button
        )


        # self.name_input = TextInput(hint_text="Enter your name", size_hint=(1, 0.2), multiline=False)
        # layout.add_widget(self.name_input)
        tribes_layout = GridLayout(cols=2, spacing=15, size_hint=(1, 0.6))
        
        for tribe in tribes:
            btn = Button(
                text=tribe,
                size_hint=(1, 0.2),
                font_name="ComicNeue-Bold.ttf",
                font_size=24,
                background_color=(0.2, 0.6, 0.8, 1)  # Blue shade
            )
            btn.bind(on_press=lambda instance, t=tribe: self.select_tribe(t))
            tribes_layout.add_widget(btn)

        layout.add_widget(tribes_layout)
        self.add_widget(layout)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def select_tribe(self, tribe):
        app = App.get_running_app()
        app.selected_tribe = tribe
        app.username = self.name_input.text if self.name_input.text.strip() else "Friend"
        self.manager.current = "topic_selection"

# Home Screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        self.title = Label(text="", font_size=28, color=(0.902, 0.905, 0.145, 0.87),font_name="ComicNeue-Bold.ttf")
        layout.add_widget(self.title)


        lesson_btn = Button(text="Start Video Lesson", size_hint=(1, 0.2))
        quiz_btn = Button(text="Take Quiz", size_hint=(1, 0.2))
        exit_btn = Button(text="Exit", size_hint=(1, 0.2))

        lesson_btn.bind(on_press=self.go_to_lessons)
        quiz_btn.bind(on_press=self.go_to_quiz)
        exit_btn.bind(on_press=lambda x: App.get_running_app().stop())

        layout.add_widget(lesson_btn)
        layout.add_widget(quiz_btn)
        layout.add_widget(exit_btn)

        self.add_widget(layout)
        
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.title.text = f"Welcome {app.username}!\nTribe: {app.selected_tribe}"

    def go_to_lessons(self, instance):
        self.manager.current = "lessons"

    def go_to_quiz(self, instance):
        self.manager.current = "quiz"


# Lessons Screen
# from kivy.uix.video import Video

class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonScreen, self).__init__(**kwargs)
        layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        self.video = Video(source="lesson2.mp4", state="play", options={'eos': 'loop'})
        layout.add_widget(self.video)

        controls = BoxLayout(size_hint=(1, 0.2), spacing=10)
        play_btn = Button(text="Play")
        pause_btn = Button(text="Pause")
        stop_btn = Button(text="Stop")

        play_btn.bind(on_press=lambda x: setattr(self.video, "state", "play"))
        pause_btn.bind(on_press=lambda x: setattr(self.video, "state", "pause"))
        stop_btn.bind(on_press=lambda x: setattr(self.video, "state", "stop"))

        controls.add_widget(play_btn)
        controls.add_widget(pause_btn)
        controls.add_widget(stop_btn)

        back_btn = Button(text="Back", size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(controls)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "home"


# Topic Selection Screen
class TopicSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        title = Label(text="Choose Topic", font_size=36, color=(0.9, 0.6, 0.2, 1))
        layout.add_widget(title)

        topics = ["Math", "General"]
        for topic in topics:
            btn = Button(
                text=topic,
                font_size=24,
                background_color=(0.2, 0.7, 0.9, 1)
            )
            btn.bind(on_press=lambda instance, t=topic: self.select_topic(t))
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_topic(self, topic):
        app = App.get_running_app()
        app.selected_topic = topic
        self.manager.current = "quiz"



# # Quiz Screen
# from kivy.app import App
# from kivy.uix.screenmanager import Screen
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.clock import Clock

# # 👇 quiz.py se data import
# from quiz import QUIZ_DATA  

# # 👇 BackgroundBoxLayout tum already bana chuki ho
# from background_layout import BackgroundBoxLayout  


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)

        # Main layout with background
        self.layout = BackgroundBoxLayout(orientation='vertical', spacing=20, padding=40)

        # Question label
        self.question_label = Label(text="", font_size=26, color=(0, 0, 0, 1))
        self.layout.add_widget(self.question_label)
        \
        self.questions = []
        self.current_index = 0
        self.score = 0

        # Option buttons
        self.option_buttons = []
        for i in range(3):  # max 3 options
            btn = Button(size_hint=(1, None), height=80, font_size=20, background_color=(1, 1, 1, 1))
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.layout.add_widget(btn)

        # Feedback label
        self.feedback_label = Label(text="", font_size=20, color=(0.2, 0.5, 0.9, 1))
        self.layout.add_widget(self.feedback_label)

        # Next button
        self.next_btn = Button(text="Next", size_hint=(1, 0.2), font_size=22)
        self.next_btn.bind(on_press=self.next_question)
        self.layout.add_widget(self.next_btn)

        # Back button
        self.back_btn = Button(text="Back to Home", size_hint=(1, 0.2), font_size=22)
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

        # State
        

    COLORS = [
        (1, 0, 0, 1),      # Bright Red
        (0, 1, 0, 1),      # Bright Green
        (0, 0, 1, 1),      # Bright Blue
        (1, 0.5, 0, 1),    # Orange
        (1, 0, 1, 1),      # Magenta
        (0, 1, 1, 1),      # Cyan
        (1, 1, 0, 1)       # Yellow
    ]
    # --- Blink effect on button ---

    def blink_button(self, button, color1, color2, times=4, interval=0.2):
        def toggle_color(dt):
            nonlocal times
            if times > 0:
                button.background_color = color1 if times % 2 == 0 else color2
                times -= 1
                Clock.schedule_once(toggle_color, interval)
            else:
                button.background_color = (1, 1, 1, 1)  # reset to white
        toggle_color(0)


    
    

    # --- Load quiz when screen opens ---
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        tribe = app.selected_tribe
        topic = app.selected_topic if hasattr(app, "selected_topic") else "General"

        # Load questions
        self.questions = QUIZ_DATA.get(tribe, {}).get(topic, [])
        self.current_index = 0
        self.score = 0

        if self.questions:
            self.show_question()
        else:
            self.question_label.text = "No quiz available for this tribe/topic."
            self.feedback_label.text = ""
            for btn in self.option_buttons:
                btn.text = ""
                btn.disabled = True
            self.next_btn.disabled = True

     # --- Show current question with random color ---
    def show_question(self):
        q = self.questions[self.current_index]

        # 👇 Random color for question text
        self.question_label.color = random.choice(self.COLORS)
        self.question_label.text = f"Q: {q['q_en']}\n{q['q_local']}"

        for i, option in enumerate(q["options_en"]):
            self.option_buttons[i].text = f"{option}\n({q['options_local'][i]})"
            self.option_buttons[i].answer_value = option
            self.option_buttons[i].background_color = (1, 1, 1, 1)
            self.option_buttons[i].disabled = False

        self.feedback_label.text = ""

    # --- Answer check ---
    def check_answer(self, instance):
        q = self.questions[self.current_index]
        if instance.answer_value == q["answer"]:
            self.score += 1
            self.feedback_label.text = "Correct!"
            self.blink_button(instance, (0, 1, 0, 1), (1, 1, 1, 1))  # green blink
        else:
            self.feedback_label.text = "Wrong!"
            self.blink_button(instance, (1, 0, 0, 1), (1, 1, 1, 1))  # red blink

        for btn in self.option_buttons:
            btn.disabled = True

    # --- Next question ---
    def next_question(self, instance):
        if self.current_index + 1 < len(self.questions):
            self.current_index += 1
            self.show_question()
        else:
            self.question_label.text = f"Quiz Finished!\nYour Score: {self.score}/{len(self.questions)}"
            self.feedback_label.text = "Great Job!" if self.score > 0 else "Keep Practicing!"
            for btn in self.option_buttons:
                btn.text = ""
                btn.disabled = True

            # self.next_btn.disabled = True
            # 👇 Change Next button to go back to topic selection
            self.next_btn.text = "Choose Another Topic"
            self.next_btn.unbind(on_press=self.next_question)
            self.next_btn.bind(on_press=self.go_topic_selection)


    # --- Go back to home ---
    def go_back(self, instance):
        self.manager.current = "topic_selection"
    def go_topic_selection(self, *args):
        self.manager.current = "topic_selection"



# Screen Manager
class TribalApp(App):
    def build(self):
        self.selected_tribe = None
        self.username = "Friend"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(TribeSelectionScreen(name="tribe"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LessonScreen(name="lessons"))
        sm.add_widget(TopicSelectionScreen(name="topic_selection"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.current = "tribe"   # ✅ Start from tribe selection
        return sm


if __name__ == "__main__":
    TribalApp().run()
