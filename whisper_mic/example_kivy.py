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
            pause=0.75,
            dynamic_energy=False,
            save_file=False,
            device=("cuda" if torch.cuda.is_available() else "cpu"),
        )
        threading.Thread(target=self.whisper_mic.transcribe_forever).start()
        self.label = Label(text=str("Say Something!"), font_size=70)
        Clock.schedule_interval(self.update_from_mic, 0.1)
        return self.label

    def update_from_mic(self, dt):
        try:
            result = self.whisper_mic.result_queue.get_nowait()
            self.label.text = str(result)
        except Exception:
            pass


if __name__ == "__main__":
    DisplaySpeechApp().run()
