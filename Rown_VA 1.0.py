import pyttsx3 
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import wolframalpha
import time
import pyautogui
import json
import requests
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


engine = pyttsx3.init()
chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
wolframalpha_app_id = '32Y4YW-HG3V874TYW'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def T12():
    if int(datetime.datetime.now().strftime("%H"))>12:
        return ("pm")
    else: 
        return ("am")

def time_():
    speak("The time is ")
    speak(datetime.datetime.now().strftime("%I:%M"))
    speak(T12())
    
def date():
    speak("Date is"+str(datetime.datetime.now().day)+"And Month is "+str(datetime.datetime.now().month)+"And the Year is"+str(datetime.datetime.now().year))
    

def greeting():
    h = datetime.datetime.now().hour
    if h >=6 and h<12:
        speak("Good Morning Sir!")
    elif h>=12 and h<18:
        speak("Good Afternoon Sir!")
    elif h>=18 and h<24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")
    speak("Rown is at your Service. How can i help you!")

def TakeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        qurey = r.recognize_google(audio,language='en-US')
        print(qurey)

    except Exception as e:
        print(e)
        print("Say that again Please!")
        return "None"
    return qurey

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('username@gmail.com','password')
    server.sendmail('username@gmail.com',to,content)
    server.close()

def correct_query():
    speak("Say something")
    result = TakeCommand().lower()
    while True:
        speak(result)
        speak("Is it Ok?")
        if 'no' in TakeCommand().lower():
            speak("Ok Say it again")
            result= TakeCommand()
        else:
            break
    return result
def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)
    try:
        battery = psutil.sensors_battery()
        speak("The Battery is")
        speak(battery.percent)
    except Exception as e:
        print(e)
        speak("You have Battery Issue")

def joke():
    speak(pyjokes.get_joke())

def ss():
    img = pyautogui.screenshot()
    img.save('D:/ss.png')





#/////////////////////////////////////////////////////////////////////////
# MAIN
if __name__ == "__main__":
    greeting()
    while True:
        qurey = TakeCommand().lower()
        if 'goodbye' in qurey:
            speak("Good Bye, See you soon")
            quit()
        if 'time' in qurey:
            time_()
        elif 'date' in qurey:
            date()
        elif 'wikipedia' in qurey:
            #speak("What do you want to search")
            qurey = qurey.replace("wikipedia","")
            speak("According To Wikipedia")
            result = wikipedia.summary(qurey,sentences = 3)
            print(result)
            speak(result)
        elif 'what can you do' in qurey:
            speak("I can tell you normal things like time and date")
            speak("I can search things on wikipedia")
            speak("I can send Email")
            speak("I can open websites")
            speak("I can open office apps like word, excel")
            speak("I can tell you a joke")
            speak("I can write and read ")
            speak("I can tell you about the CPU and Battery Status")
            speak("I can find a location")
            speak("I can do the calculation")
            speak("I can tell the News")
            speak("I can shut down your system")
        elif 'send email' in qurey:
            try:
                speak("What should I say?")
                content= correct_query()
                speak("Who is the receiver?")
                receiver = correct_query()
                sendEmail(receiver,content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry Unable to Send The Email")
        elif 'search in chrome' in qurey:
            speak("which website shoud i open?")
            search = TakeCommand().lower()
            if 'youtube' in search:
                speak("What do you want to search in youtube")
                search=TakeCommand().lower()
                wb.get(chromepath).open('https://www.youtube.com/results?search_query='+search)
            elif 'google' in search:
                speak("What do you want to search in google")
                search=TakeCommand().lower()
                wb.get(chromepath).open('https://www.google.com/search?q='+search)
            else:
               wb.get(chromepath).open_new_tab(search+".com")
        elif 'cpu' in qurey:
            cpu()
        elif 'joke' in qurey:
            joke()
        elif 'word' in qurey:
            speak("Opening MS WORD.....")
            ms_word = r'C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE'
            os.startfile(ms_word)
        elif 'powerpoint' in qurey:
            speak("Opening Powerpoint.....")
            ms_pp = r'C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE'
            os.startfile(ms_pp)
        elif 'excel' in qurey:
            speak("Opening MS Execel.....")
            ms_excel = r'C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE'
            os.startfile(ms_excel)
        elif 'write a note' in qurey:
            speak("What do you want to write")
            txt = correct_query()
            file = open('Desktop/notes.txt','w')
            print(txt)
            file.write(txt)
            speak("Successfully saved")
        elif 'read a note' in qurey:
            speak("Let me check if you have a note exist")
            try:
                file = open('Desktop/notes.txt','r')
                speak("Found one and the note is: ")
                speak(file.read())
            except Exception as e:
                print(e)
                speak("No such file exist")
        elif 'screenshot' in qurey:
            ss()
            speak("Would you like to see")
            if 'yes' or 'sure' in TakeCommand():
                ss = r'D:/ss.png'
                os.startfile(ss)
        elif 'remeber that' in qurey:
            speak("What should i remeber")
            txt=TakeCommand()
            file= open('Desktop/memory.txt','w')
            file.write(txt)
            file.close()
        elif 'do you remember anything' in qurey:
            try:
                speak('Let me rememeber')
                file = open('Desktop/memory.txt','w')
                speak(file.read())
            except Exception as e:
                print(e)
                speak("No memory found")
        elif 'where is' in qurey:
            qurey = qurey.replace("where is","")
            speak("let me check")
            wb.get(chromepath).open('https://www.google.com/maps/place/'+qurey)
        elif 'calculate' in qurey:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = qurey.lower().split().index('calculate')
            qurey = qurey.split()[indx + 1:]
            res = client.query(''.join(qurey))
            answer = next(res.results).text
            print("The answer is "+answer)
            speak("The answer is "+answer)
        elif 'stop listening' in qurey:
            speak("How much time you want me to stop listening?")
            ans = int(TakeCommand().replace("minutes",""))
            print("Sleeping for "+str(ans)+"mints")
            speak("Sleeping for "+str(ans)+"mints")
            time.sleep(ans*60)
            speak("I am Up now!!!")
        elif 'news' in qurey:
            try:
                jsonobj = urlopen("http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=32a649f43a2e4075b29572da989ccc42")
                data = json.load(jsonobj)
                i=1
                speak("Here is some headlines from Tech")
                print("===============TOP Story================\n")
                for item in data['articles']:
                    print(str(i)+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i+=1
            except Exception as e:
                print(e)
                speak("Unable to find a News!!!")
        elif 'what is ' or 'who is ' in qurey:
            client=wolframalpha.Client(wolframalpha_app_id)
            res = client.query(qurey)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No Result")
        elif 'shutdown' in qurey:
            os.system("shutdown -l")    