# Tango Bots

> CSCI-455: Embedded Systems (Robotics) - Spring 2022 @ Montana State University

## Running the Code

There are two versions/paths to comunicate with the robot: Through the keyboard (`tkinter-app`) or speaking into the microphone (`speech2text`). You must pass one of these commands as the first parameter to the `main.py` file.

***Speech2Text***:

```bash
python main.py speech2text
```

***Tkinter App***:

```bash
python main.py tkinter-app
```

## tkinter App

### Key Bindings

<kbd>space</kbd> will kill the running app and stop the robot.

#### Head

| Action | Key |
| :-- | :--: |
| Move head up | <kbd>w</kbd> |
| Move head down | <kbd>s</kbd> |
| Pan head left | <kbd>a</kbd> |
| Pan head right | <kbd>d</kbd> |

#### Waist

| Action | Key |
| :-- | :--: |
| Rotate left | <kbd>z</kbd> |
| Rotate right | <kbd>c</kbd> |
| Center waist | <kbd>x</kbd> |

#### Wheels

| Action | Key |
| :-- | :--: |
| Forward | <kbd>Up</kbd> |
| Backwards | <kbd>Down</kbd> |
| Turn Left | <kbd>Left</kbd> |
| Turn Right | <kbd>Right</kbd> |
| Stop | <kbd>q</kbd> |

#### Speed

| Action | Key |
| :-- | :--: |
| Speed level one: `100` | <kbd>j</kbd> |
| Speed level two: `500` | <kbd>k</kbd> |
| Speed level three: `800` | <kbd>l</kbd> |

## Speech2Text

### Setup Steps

you need to install this to do remote desk

```bash
sudo apt-get install xrdp  
```

The following you need for setting up the Text To Speech (speech.py and speech2.py)

```bash
pip install pyttsx3
sudo apt-get update && sudo apt-get install espeak
sudo apt-get install python-espeak
```

The rest of these steps are to get speech recognition working

```bash
pip install SpeechRecognition
sudo apt-get install flac
sudo apt-get update 
sudo apt-get upgrade 
sudo apt-get install portaudio19-dev 
sudo pip install pyaudio
```

### Example Files

#### `speech.py`

```python
import pyttsx3

engine = pyttsx3.init()

voice_num = 2
text_to_say = "Hello Robot, Class! I am Tango!"

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voice_num].id)

engine.say(text_to_say)
engine.runAndWait()
```

#### `speech2.py`

```python
import pyttsx3

engine = pyttsx3.init()

# change voice

# getting details of current voice
voices = engine.getProperty('voices')      

for i in range(10,18):
    engine.setProperty('voice', voices[i].id)
    print(engine.getProperty("voice"))
    engine.setProperty('rate', 150)

    # say something

    engine.say("Pick me, pick me! My voice is number " + str(i))
    engine.setProperty('rate', 250)
    print(engine.getProperty("rate"))
    engine.say("faster rate, Pick me, pick me! My voice is number " + str(i))

    engine.runAndWait()
```

#### `speechRecTest2.py`

```python
import speech_recognition as sr


listening = True
while listening:
    with sr.Microphone() as source:
        r= sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        r.dyanmic_energythreshhold = 3000
        
        try:
            print("listening")
            audio = r.listen(source)            
            print("Got audio")
            word = r.recognize_google(audio)
            print(word)
        except sr.UnknownValueError:
            print("Don't knoe that werd")
            
#mic = sr.Microphone()

#with mic as source:
#	au = r.listen(source)

#print("here")
#word = r.recognize_google(au)
#print ("here", word)
```