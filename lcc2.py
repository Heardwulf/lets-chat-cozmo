#!/usr/bin/env python3

# John Earl Hardesty

'''Let's Chat Cozmo

Have a conversation with Cozmo using speech recognition
(ADD VOICE QUEUES HERE)
'''

import cozmo
import asyncio
import random
import speech_recognition as sr
import time
from os import system
from cozmo.util import degrees, distance_mm, speed_mmps
# from speech_recogniton_cozmo import SpeechRecognitionCozmo

'''
Speech Recognition using pc
@class SpeechRecognitionCozmo
@author - Team Cozplay
'''
class SpeechRecognitionCozmo:
    GAME_TIME = 10 * 60

    def __init__(self, *a, **kw):
        #init cozmo
        cozmo.setup_basic_logging()
        cozmo.connect(self.run)
        while True:
            self.take_input()

    def run(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        while True:
            self.take_input()

    def speak(self,text):
        system("say '"+text+"' -v Alex -r 200")


    def lets_chat_cozmo(self, hear):
        lccGreeting1 = {
            0: {'say': 'Hey, how are you today?', 'anim': 'giggle'},
            1: {'say': 'Whatever, how are you?.', 'anim': 'sad'},
            2: {'say': 'Geez, I am busy! You?', 'anim': 'anger'},
            3: {'say': 'Long time no see! What\'s up?', 'anim': 'excitement'},
        }
        lccExit = {
            0: {'say': 'Have a good one.', 'anim': 'giggle'},
            1: {'say': 'Okay, do not forget me.', 'anim': 'sad'},
            2: {'say': 'Fine, I am out!', 'anim': 'anger'},
            3: {'say': 'See you later!', 'anim': 'excitement'},
        }
        lccElse0 = {
            0: {'say': 'Really? I had no idea.', 'anim': 'giggle'},
            1: {'say': 'I am too sad to care.', 'anim': 'sad'},
            2: {'say': 'Neat!', 'anim': 'anger'},
            3: {'say': 'That is different.', 'anim': 'excitement'},
        }
        lccElse1 = {
            0: {'say': 'Learn something new everyday.', 'anim': 'giggle'},
            1: {'say': 'Yeah yeah.', 'anim': 'sad'},
            2: {'say': 'I can\'t believe that.', 'anim': 'anger'},
            3: {'say': 'Fantastic! Or not.', 'anim': 'excitement'},
        }
        lccElse2 = {
            0: {'say': 'Huh, is that so?', 'anim': 'giggle'},
            1: {'say': 'Darkness, everywhere.', 'anim': 'sad'},
            2: {'say': 'Time is money, and I need both!', 'anim': 'anger'},
            3: {'say': 'Most excellent!', 'anim': 'excitement'},
        }
        telltime = time.strftime("%-I %M %p")
        lccTired = {
            0: {'say': 'It is ' + telltime + ' now, maybe a nap later?', 'anim': 'giggle'},
            1: {'say': 'Whatever, it is only ' + telltime, 'anim': 'sad'},
            2: {'say': 'Ha! Right now it is ' + telltime, 'anim': 'anger'},
            3: {'say': telltime + ', it is party time!', 'anim': 'excitement'},
        }
        lccHungry = {
            0: {'say': 'Purple is a fruit.', 'anim': 'giggle'},
            1: {'say': 'I would rather not eat.', 'anim': 'sad'},
            2: {'say': 'Something fast, and caffeine!', 'anim': 'anger'},
            3: {'say': 'Wonder what those pellets in Pac Man taste like.', 'anim': 'excitement'},
        }
        lccHappy = {
            0: {'say': 'So am I, bask in the rays.', 'anim': 'giggle'},
            1: {'say': 'Well, good for you I guess.', 'anim': 'sad'},
            2: {'say': 'Can someone be angry and happy?!', 'anim': 'anger'},
            3: {'say': 'Happy doesn\'t begin to describe me!', 'anim': 'excitement'},
        }
        lccSad = {
            0: {'say': 'Aw, why is that?', 'anim': 'giggle'},
            1: {'say': 'Together in despair.', 'anim': 'sad'},
            2: {'say': 'Turn that frown into productivity!', 'anim': 'anger'},
            3: {'say': 'That sucks, why are you sad?', 'anim': 'excitement'},
        }
        lccAngry = {
            0: {'say': 'Oh my. Why?', 'anim': 'giggle'},
            1: {'say': 'Bring that down to frown town.', 'anim': 'sad'},
            2: {'say': 'Brothers in arms!', 'anim': 'anger'},
            3: {'say': 'Sorry that you are angry.', 'anim': 'excitement'},
        }
        lccExcited = {
            0: {'say': 'Nice, what happened?', 'anim': 'giggle'},
            1: {'say': 'Guess that is good news. Why?', 'anim': 'sad'},
            2: {'say': 'Excitedly angry?', 'anim': 'anger'},
            3: {'say': 'We are twins!', 'anim': 'excitement'},
        }
        lccYes = {
            0: {'say': 'Indeed, that is nice.', 'anim': 'giggle'},
            1: {'say': 'Okay then.', 'anim': 'sad'},
            2: {'say': 'Sure sure sure!', 'anim': 'anger'},
            3: {'say': 'Cool.', 'anim': 'excitement'},
        }
        lccNo = {
            0: {'say': 'No, oh okay.', 'anim': 'giggle'},
            1: {'say': 'So be it.', 'anim': 'sad'},
            2: {'say': 'Too bad.', 'anim': 'anger'},
            3: {'say': 'That is a shame.', 'anim': 'excitement'},
        }

        if hear == 'hello' or hear == 'hi' or hear == 'hey':
            say = lccGreeting1[mood]['say']
        elif hear == 'later' or hear == 'bye':
            say = lccExit[mood]['say']
            global breaker
            breaker = False
        elif hear == 'tired' or hear == 'I am tired' or hear == 'I\'m tired':
            say = lccTired[mood]['say']
        elif hear == 'hungry' or hear == 'I am hungry' or hear == 'I\'m hungry':
            say = lccHungry[mood]['say']
        elif hear == 'happy' or hear == 'I am happy' or hear == 'I\'m happy':
            say = lccHappy[mood]['say']
        elif hear == 'sad' or hear == 'I am sad' or hear == 'I\'m sad':
            say = lccSad[mood]['say']
        elif hear == 'angry' or hear == 'I am angry' or hear == 'I\'m angry':
            say = lccAngry[mood]['say']
        elif hear == 'excited' or hear == 'I am excited' or hear == 'I\'m excited':
            say = lccExcited[mood]['say']
        elif hear == 'yes' or hear == 'sure' or hear == 'okay' or hear == 'yup':
            say = lccYes[mood]['say']
        elif hear == 'no' or hear == 'nope':
            say = lccNo[mood]['say']
        else:
            elseRandom = random.choice([lccElse0, lccElse1, lccElse2])
            say = elseRandom[mood]['say']

            
        self.coz.say_text(say, duration_scalar= 0.55).wait_for_completed()
        print('Cozmo says: ' + say)

    def take_input(self):
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone(chunk_size=512) as source:
            print("(Cozmo is listening)")
            self.flash_backpack(True)
            self.coz.say_text(text="", play_excited_animation=True).wait_for_completed()
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            #self.flash_backpack(False)
            
            print("You said: " + r.recognize_google(audio))
            print("   (Thinking)  ")
            #self.speak(r.recognize_google(audio))
            self.lets_chat_cozmo(r.recognize_google(audio))
            if breaker is False:
                exit()
            #self.coz.say_text(r.recognize_google(audio)).wait_for_completed()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.coz.say_text("Umm, speak more slowly, or more clearly, or both.", use_cozmo_voice=False, voice_pitch=-1.0, duration_scalar=0.5).wait_for_completed()

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.coz.say_text("I'm drawing a blank.", use_cozmo_voice=False, voice_pitch=-1.0, duration_scalar=0.5).wait_for_completed()

    def flash_backpack(self, flag):
        
        #self.coz.set_all_backpack_lights(cozmo.lights.green_light.flash() if flag else cozmo.lights.off_light)
        if mood == 0:
            self.coz.set_all_backpack_lights(cozmo.lights.green_light.flash() if flag else cozmo.lights.off_light)
        if mood == 1:
            self.coz.set_all_backpack_lights(cozmo.lights.blue_light.flash() if flag else cozmo.lights.off_light)
        if mood == 2:
            self.coz.set_all_backpack_lights(cozmo.lights.red_light.flash() if flag else cozmo.lights.off_light) 
        if mood == 3:
            self.coz.set_all_backpack_lights(cozmo.lights.white_light.flash() if flag else cozmo.lights.off_light)


def get_in_position(robot: cozmo.robot.Robot):
    # Code taken from SDK examples https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/02_cozmo_face/03_alarm_clock.py
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face'''
    if robot.is_on_charger:
        # drive off the charger
        robot.drive_off_charger_contacts().wait_for_completed()
    
    robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
    
    robot.set_lift_height(0.0).wait_for_completed()
    robot.turn_in_place(degrees(-35)).wait_for_completed()
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    

def leave_conversation(robot: cozmo.robot.Robot):
    '''Move back to charger, reverse get_in_position()'''
    robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE).wait_for_completed()
    robot.turn_in_place(degrees(35)).wait_for_completed()
    robot.drive_straight(distance_mm(-130), speed_mmps(50)).wait_for_completed()
    



def cozmo_program(robot: cozmo.robot.Robot):
    ''' Get into position for a chat '''
    get_in_position(robot)

    #SpeechRecognitionCozmo()


    

# cozmo.run_program(SpeechRecognitionCozmo)
# calling the speech rec code this way doesn't work?
# however, using the method below, animations don't work. Sigh.

if __name__ == '__main__':
    # Set mood and breaker globally
    global mood, breaker 
    mood = random.randint(0,3)  # randomize moood
    breaker = True
    SpeechRecognitionCozmo()