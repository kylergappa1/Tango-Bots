# speech2text.py

import speech_recognition as sr
import threading
from .tango_bot import TangBotController
from .log import log

PHRASE_BOT_DICT = {
    'head up': 'moveHeadUp',
    'head down': 'moveHeadDown',
    'head left': 'moveHeadLeft',
    'head right': 'moveHeadRight',
    'head center': 'centerHead',
    'body left': 'moveWaistLeft',
    'body right': 'moveWaistRight',
    'body center': 'centerWaist',
    'forward': 'increaseWheelSpeed',
    'reverse': 'decreaseWheelSpeed',
    'turn left': 'turnLeft',
    'turn right': 'turnRight',
    'stop': 'stop'
}

class Speech2Text:

    bot: TangBotController
    running: bool
    recognizer: sr.Recognizer
    microphone: sr.Microphone
    audio_recognizing_thread: threading.Thread

    # constructor
    def __init__(self, bot: TangBotController):
        self.bot = bot
        self.running = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_recognizing_thread = threading.Thread(target=self.threaded_audio_transcribing, daemon=True)

    def recognize_speech_from_mic(self):
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, 0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=2)
        except sr.WaitTimeoutError:
            return None
        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught
        transcription = None
        try:
            transcription = self.recognizer.recognize_google(audio)
            print(transcription)
        except sr.RequestError as err:
            # API was unreachable or unresponsive
            print("API was unreachable or unresponsive.\n", err)
        except sr.UnknownValueError as err:
            # speech was unintelligible
            print("Unknown word")
        return transcription

    def threaded_audio_transcribing(self):
        while True:
            if self.running is False: 
                break
            transcription: str = self.recognize_speech_from_mic()
            if transcription is None: 
                continue
            log.info("Transcription: %s", transcription)
            transcription = transcription.lower()
            print("Converted: ", transcription)
            # call TangoBot method based on phrase transcription
            if transcription not in PHRASE_BOT_DICT.keys(): 
                continue
            attr_name = PHRASE_BOT_DICT[transcription]
            if not hasattr(self.bot, attr_name):
                continue
            obj_attr = getattr(self.bot, attr_name)
            obj_attr()

    def start(self):
        self.running = True
        self.audio_recognizing_thread.start()
        try:
            while True:
                if self.running is False: break
        except:
            print()
            pass
        self.bot.stop()
        self.running = False
        self.audio_recognizing_thread.join()


# END
