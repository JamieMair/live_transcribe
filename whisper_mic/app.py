from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
import torch
from whisper_mic.whisper_mic import WhisperMic
import threading


class DisplaySpeechApp(App):
    label = None
    whisper_mic = None

    def build(self):
        self.whisper_mic = WhisperMic(
            model="base",
            english=True,
            verbose=False,
            energy=300,
            pause=0.4,
            dynamic_energy=False,
            save_file=False,
            device=("cuda" if torch.cuda.is_available() else "cpu"),
        )
        threading.Thread(target=self.whisper_mic.transcribe_forever).start()
        self.label = Label(
            text=str("Say Something!"),
            font_size=70,
            size_hint=(1, None),
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.label.bind(
            width=lambda *x: self.label.setter("text_size")(
                self.label, (self.label.width, None)
            ),
            texture_size=lambda *x: self.label.setter("height")(
                self.label, self.label.texture_size[1]
            ),
        )
        Clock.schedule_interval(self.update_from_mic, 0.2)
        return self.label

    def update_from_mic(self, dt):
        try:
            result = self.whisper_mic.result_queue.get_nowait()
            if str(result).strip() != "":
                self.label.text = str(result)
        except Exception:
            pass


if __name__ == "__main__":
    DisplaySpeechApp().run()
