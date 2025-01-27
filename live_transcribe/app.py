from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
import torch
from live_transcribe.live_transcribe import LiveTranscribe
import threading


class DisplaySpeechApp(App):
    label = None
    live_transcribe = None
    num_lines = 1
    is_first = True

    def build(self):
        self.live_transcribe = LiveTranscribe(
            model="base",
            english=True,
            verbose=False,
            energy=280,
            pause=0.4,
            dynamic_energy=False,
            save_file=False,
            device=("cuda" if torch.cuda.is_available() else "cpu"),
        )
        threading.Thread(target=self.live_transcribe.transcribe_forever).start()
        self.label = Label(
            text=str("..."),
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
        Clock.schedule_interval(self.update_from_mic, 1.0 / 60)
        return self.label

    def update_from_mic(self, dt):
        max_lines = 6
        try:
            result = self.live_transcribe.result_queue.get_nowait()
            result = str(result)
            if result.strip() != "":
                if self.is_first:
                    self.label.text = result
                    self.is_first = False
                    return
                new_text = self.label.text + "\n" + result
                self.num_lines += 1
                if self.num_lines > max_lines:
                    remaining_sentences = new_text.split("\n")[-max_lines:]
                    new_text = "\n".join(remaining_sentences)
                    self.num_lines = len(remaining_sentences)

                self.label.text = new_text
        except Exception:
            pass


if __name__ == "__main__":
    DisplaySpeechApp().run()
