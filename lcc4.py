#!/usr/bin/env python3
# John Earl Hardesty

'''Let's Chat Cozmo

Have a conversation with Cozmo using speech recognition
Cozmo understands: hi/hey/hello, later/bye, tired, hungry
    happy, sad, angry, excited, yes, no

Last-minute rewrite using an example from rproenca at Anki forums
https://forums.anki.com/t/controlling-cozmo-via-voice-commands/1183
'''



import speech_recognition as sr
import cozmo
import random
import time # used for the tired response
import os
from cozmo.util import degrees, distance_mm, speed_mmps # used for movement
from PIL import Image #used for face images
import sys

# Globals, I know I shouldn't used them.
global mood, asked, breaker
mood = 4
asked = False
breaker = True

def cls(): 
    # Thanks to stackoverflow for this
    # https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
    os.system('cls' if os.name=='nt' else 'clear')

def get_in_position(robot: cozmo.robot.Robot):
    # Code taken from SDK examples https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/02_cozmo_face/03_alarm_clock.py
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face'''
    if robot.is_on_charger:
        # drive off the charger
        robot.drive_off_charger_contacts().wait_for_completed()
    
    robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
    
    robot.set_lift_height(0.0).wait_for_completed()
    robot.turn_in_place(degrees(-30)).wait_for_completed()
    #robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    robot.set_head_angle(degrees(25)).wait_for_completed()

def flash_backpack(robot: cozmo.robot.Robot):
    global mood
    # Change backpack colors based on mood
    if mood == 0:
        robot.set_all_backpack_lights(cozmo.lights.green_light.flash())
    elif mood == 1:
        robot.set_all_backpack_lights(cozmo.lights.blue_light.flash())
    elif mood == 2:
        robot.set_all_backpack_lights(cozmo.lights.red_light.flash())
    elif mood == 3:
        robot.set_all_backpack_lights(cozmo.lights.white_light.flash())
    else:
        robot.set_all_backpack_lights(cozmo.lights.off)

def react(robot, animate):
    animateNow = 'anim_neutral_eyes_01'
    
    if animate == 'error':
        animateNow = 'anim_gif_idk_01'
    elif animate == 'angry':
        animateNow = 'anim_memorymatch_failhand_01'
    elif animate == 'happy':
        animateNow = 'anim_sparking_success_01'
    elif animate == 'sad':
        animateNow = 'anim_energy_getout_01'
    elif animate == 'excited':
        animateNow = 'anim_fistbump_success_01'
    elif animate == 'confused':
        animateNow = 'anim_gif_idk_01'
    elif animate == 'thinking':
        animateNow = 'anim_mm_thinking'
    elif animate == 'normal':
        animateNow = 'anim_neutral_eyes_01'
    else:
        animateNow = 'anim_neutral_eyes_01'

    robot.play_anim(animateNow, in_parallel = True).wait_for_completed()

def faceImage(robot, face): 
        # Takes the variable face and displays a pre-defined image of it
        # Very proud of this, so happy I found another sample code that didn't use asyncio
        image = Image.open('lcc_' + face + '.png')
        image = image.resize(cozmo.oled_face.dimensions(), Image.NEAREST)
        image = cozmo.oled_face.convert_image_to_screen_data(image)

        #time.sleep(2)
        robot.display_oled_face_image(screen_data = image, duration_ms = 2000.0)

def hear(source, r, robot):
    audio = r.listen(source)
    try:
        recognized = r.recognize_google(audio)
        print("You said: " + recognized)
        print("   (Thinking)  ")
        
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
            0: {'say': 'I hear ya.', 'anim': 'giggle'},
            1: {'say': 'Well, good for you I guess.', 'anim': 'sad'},
            2: {'say': 'Can someone be angry and happy?!', 'anim': 'anger'},
            3: {'say': 'Happy doesn\'t begin to describe me!', 'anim': 'excitement'},
        }
        lccSad = {
            0: {'say': 'Aw, why is that?', 'anim': 'giggle'},
            1: {'say': 'Tell me about it..', 'anim': 'sad'},
            2: {'say': 'Turn that frown into productivity!', 'anim': 'anger'},
            3: {'say': 'That sucks, why are you sad?', 'anim': 'excitement'},
        }
        lccAngry = {
            0: {'say': 'Oh my. Why?', 'anim': 'giggle'},
            1: {'say': 'Bring that down to frown town.', 'anim': 'sad'},
            2: {'say': 'I heard you!', 'anim': 'anger'},
            3: {'say': 'Sorry that you are angry.', 'anim': 'excitement'},
        }
        lccExcited = {
            0: {'say': 'Nice, what happened?', 'anim': 'giggle'},
            1: {'say': 'Guess that is good news. Why?', 'anim': 'sad'},
            2: {'say': 'Excitedly angry?', 'anim': 'anger'},
            3: {'say': 'Tell me about it!', 'anim': 'excitement'},
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

        
        global mood, asked
        if mood == 4:

            if recognized == 'happy' or recognized == 'I am happy' or recognized == 'I\'m happy':
                #global mood
                mood = 0
                say = 'So am I, bask in the rays. How are you?'
                
            elif recognized == 'sad' or recognized == 'I am sad' or recognized == 'I\'m sad':
                #global mood
                mood = 1
                say = 'Together in despair. Why are you down?'
            elif recognized == 'angry' or recognized == 'I am angry' or recognized == 'I\'m angry':
                #global mood
                mood = 2
                say = 'Brothers in arms! Why are you angry?!'
            elif recognized == 'excited' or recognized == 'I am excited' or recognized == 'I\'m excited':
                #global mood
                mood = 3
                say = 'We are twins! What about!?'
            else:
                say = 'I don\'t understand; are you happy, sad, angry, or excited?'
            #self.coz.say_text(say, duration_scalar= 0.55).wait_for_completed()
            #print('Cozmo says: ' + say)
        else:
            if recognized == 'hello' or recognized == 'hi' or recognized == 'hey':
                say = lccGreeting1[mood]['say']
            elif recognized == 'later' or recognized == 'bye':
                say = lccExit[mood]['say']
                global breaker
                breaker = False
            elif recognized == 'tired' or recognized == 'I am tired' or recognized == 'I\'m tired':
                say = lccTired[mood]['say']
            elif recognized == 'hungry' or recognized == 'I am hungry' or recognized == 'I\'m hungry':
                say = lccHungry[mood]['say']
            elif recognized == 'happy' or recognized == 'I am happy' or recognized == 'I\'m happy':
                say = lccHappy[mood]['say']
            elif recognized == 'sad' or recognized == 'I am sad' or recognized == 'I\'m sad':
                say = lccSad[mood]['say']
            elif recognized == 'angry' or recognized == 'I am angry' or recognized == 'I\'m angry':
                say = lccAngry[mood]['say']
            elif recognized == 'excited' or recognized == 'I am excited' or recognized == 'I\'m excited':
                say = lccExcited[mood]['say']
            elif recognized == 'yes' or recognized == 'sure' or recognized == 'okay' or recognized == 'yup':
                say = lccYes[mood]['say']
            elif recognized == 'no' or recognized == 'nope':
                say = lccNo[mood]['say']
            else:
                elseRandom = random.choice([lccElse0, lccElse1, lccElse2])
                say = elseRandom[mood]['say']

        # Mood affects voice characteristics
        isExcited = False

        if mood == 0 and asked is False:
            faceImage(robot, 'happy')
            voicePitch = 0.0
            voiceDuration = 0.65
            react(robot, 'happy')
            asked = True
        elif mood == 1 and asked is False:
            voicePitch = -0.9
            voiceDuration = 0.80
            faceImage(robot, 'sad')
            react(robot, 'sad')
            asked = True
        elif mood == 2 and asked is False:
            voicePitch = 0.25
            voiceDuration = 0.6
            faceImage(robot, 'angry')
            react(robot, 'angry')
            asked = True
        elif mood == 3 and asked is False:
            voicePitch = 0.60
            voiceDuration = 0.5
            isExcited = True
            faceImage(robot, 'excited')
            react(robot, 'excited')
            asked = True
        else:
            voiceDuration = 0.55 # higher is slower
            voicePitch = 0 # -1.0 to 1.0
        
        print('Cozmo says: ' + say)
        if mood < 4:
            flash_backpack(robot)
        if breaker is False:
            faceImage(robot, 'bye')

        #react(robot, 'normal')
        robot.say_text(say, voice_pitch = voicePitch, duration_scalar= voiceDuration, play_excited_animation= isExcited, in_parallel = True).wait_for_completed()

        
    except sr.UnknownValueError:
        print("  [Google Speech Recognition could not understand audio]")
        react(robot, 'error')
        error1 = 'Umm, speak more slowly, or more clearly, or both.'
        faceImage(robot, 'error')
        print('Error says: ' + error1)
        robot.say_text(error1, use_cozmo_voice=False, voice_pitch=-1.0, duration_scalar=0.5, in_parallel = True).wait_for_completed()
    except sr.RequestError as e:
        print("  [Could not request results from Google Speech Recognition service; {0}]".format(e))
        react(robot, 'error')
        error2 = "I am drawing a blank."
        faceImage(robot, 'error')
        print('Error says: ' + error2)
        robot.say_text(error2, use_cozmo_voice=False, voice_pitch=-1.0, duration_scalar=0.5, in_parallel = True).wait_for_completed()



def run(sdk_conn):
    '''The run method runs once the Cozmo SDK is connected.'''
    robot = sdk_conn.wait_for_robot()
    try:
        # Stupid depreciation error, move this to next section
        #print("Cozmo responds to; hello, bye, yes, no, tired, angry, happy, sad, excited.")
        #print(" ")
        get_in_position(robot)
        r = sr.Recognizer()
        
        global mood, asked, breaker

        if mood > 3 and asked is False:
            cls()
            print("Let's Chat Cozmo :::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
            print("Cozmo responds to; hello, bye, yes, no, tired, angry, happy, sad, excited.")
            print(" ")
            faceImage(robot, 'hello')
            askMood = 'Hello, how are you feeling today?'
            print(askMood)
            robot.say_text(askMood, duration_scalar= 0.55, in_parallel = True).wait_for_completed()
            print("   (Listening...)")
            

        with sr.Microphone() as source:
            while breaker:
                hear(source, r, robot)
                print("   (Listening...)")
                #react(robot, 'thinking')
                recognized = None
                if breaker is False:
                    if mood == 0:
                        react(robot, 'happy')
                    elif mood == 1:
                        react(robot, 'sad')
                    elif mood == 2:
                        react(robot, 'angry')
                    elif mood == 3:
                        react(robot, 'excited')
                    print('Bye!')


    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    


if __name__ == "__main__":
    cozmo.setup_basic_logging()
    try:
        #cozmo.connect_with_tkviewer(run, force_on_top=False)
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        exit("A connection error occurred: %s" % e)