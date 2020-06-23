from os import system, name
import os
from collections import Counter
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
import sys
import json
import random
import string
import re

#initialize arrays
final_video_tags = []
finished_video_urls = []
todo_urls = []

#initialize counters
mode = 'none'
reattempted_urls = 0
urls_processed = 1
videos_proccessed = 0
usertagcount = 0

#init_settings
totaliterations = 0
initial_video_url = 'none'
currentiteration = 1
totalurlcount = 0

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def urlquestion():
    print('Input Youtube.com full video URL ')
    global initial_video_url
    initial_video_url = input('#')

def parse_strlist(sl):
    clean = re.sub("[\[\],\s]","",sl)
    splitted = re.split("[\'\"]",clean)
    values_only = [s for s in splitted if s != '']
    return values_only


def counter(method):
    if method == "video":
        global videos_proccessed
        videos_proccessed += 1
    if method == "reattempted_urls":
        global reattempted_urls
        reattempted_urls += 1
    if method == "url":
        global urls_processed
        urls_processed += 1
    if method == "iteration":
        global currentiteration
        currentiteration += 1

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



def getYoutubeTags(url):
    counter('video')
    request = requests.get(url)
    html = BeautifulSoup(request.content, features='html.parser')
    tags = html.find_all("meta", property="og:video:tag")
    for tag in tags:
        final_video_tags.append(tag['content'])

def getPageData(url):
    counter('url')
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'),features="html.parser"):
        if link.has_attr('href'):
            probie = link['href']
            prefix = '/watch?v='
            if prefix in probie:
                newurl = 'https://www.youtube.com' + probie
                addUrl(newurl)


def addUrl(url):
    if url not in finished_video_urls:
        todo_urls.append(url)
    else:
        global reattempted_urls
        counter('reattempted_urls')


def check_empty_queue():
    if len(todo_urls) == 0:
        print('queue has ended... waiting 5 seconds for recheck')
        time.sleep(5)
        if len(todo_urls) == 0:
            print('queue has stabilized, terminating program')
            shutdown()
            return True
            quit()
        else:
            return False
    else:
        return False

def display_iterations():
    clear_screen()
    if mode == 2: #display iteration count
        print('___________ITERATION ' + str(currentiteration) + '/' + str(totaliterations) + '___________')
        print('*  MODE: Count by Iterations')
        print('*  TAGS IN ARRAY : ' + str(len(final_video_tags)))
        print('*  URLS PROCESSED : ' + str(urls_processed))
        print('*  VIDEOS PROCESSED : ' + str(videos_proccessed))
        print('*  URLS REENCOUNTERED : ' + str(reattempted_urls))
        print('*  VIDEOS IN QUEUE : ' + str(len(todo_urls)))
        print('___________' + str(round((currentiteration / totaliterations),2)*100) + '% complete___________')
    elif mode == 1: #display tags count
        print('___________TAG ' + str(len(final_video_tags)) + '/' + str(usertagcount) + '___________')
        print('*  MODE: Count by Tags')
        print('*  TAGS IN ARRAY : ' + str(len(final_video_tags)))
        print('*  URLS PROCESSED : ' + str(urls_processed))
        print('*  VIDEOS PROCESSED : ' + str(videos_proccessed))
        print('*  URLS REENCOUNTERED : ' + str(reattempted_urls))
        print('*  VIDEOS IN QUEUE : ' + str(len(todo_urls)))
        print('___________' + str(round(((len(final_video_tags) + 1) / usertagcount),2)*100) + '% complete___________')





def shutdown():
    if mode == 1 and len(final_video_tags) > usertagcount:
        newsplice = len(final_video_tags) - int(usertagcount)
        del final_video_tags[:newsplice]
    print('Shutting Down')
    final_video_tags_json = json.dumps(final_video_tags)
    todo_urls_json = json.dumps(todo_urls)
    finished_video_urls_json = json.dumps(finished_video_urls)
    newfoldername = randomString()
    os.mkdir(newfoldername)
    os.chdir(newfoldername)
    with open('finalvideotags.json', 'w') as f:
        json.dump(final_video_tags_json,f)
    with open('todo_urls.json', 'w') as f:
        json.dump(todo_urls_json,f)
    with open('finished_video_urls.json', 'w') as f:
        json.dump(finished_video_urls_json,f)
    print('Iteration compilation has been saved as ' + newfoldername)



def worker(method):
    if method == 2: #count by iterations
        #notify user of new iteration and statistics
        display_iterations()
        if totaliterations == currentiteration:
            display_iterations()
            print('Software is terminating due to finishing iterations')
            shutdown()
        else:
            #first video
            if currentiteration == 1:
                getPageData(initial_video_url)
                getYoutubeTags(initial_video_url)
                global finished_video_urls
                finished_video_urls.append(initial_video_url)
                counter('iteration')
                main(mode)
            else:
                #followon videos
                if totaliterations == currentiteration:
                    print(currentiteration + totaliterations)
                    display_iterations()
                    shutdown()
                    quit()
                else:
                    if check_empty_queue() == False:
                        selectedvideo = todo_urls.pop()
                        getPageData(selectedvideo)
                        getYoutubeTags(selectedvideo)
                        finished_video_urls.append(selectedvideo)
                        counter('iteration')
                        main(mode)
    elif method == 1: #count by tags
        if len(final_video_tags) >= usertagcount:
            display_iterations()
            shutdown()
            quit()
        else:
            if len(final_video_tags) == 0:
                # first video
                getPageData(initial_video_url)
                getYoutubeTags(initial_video_url)
                finished_video_urls.append(initial_video_url)
                counter('iteration')
                display_iterations()
                main(mode)
            else:
                #followon videos
                if check_empty_queue() == False:
                    selectedvideo = todo_urls.pop()
                    getPageData(selectedvideo)
                    getYoutubeTags(selectedvideo)
                    finished_video_urls.append(selectedvideo)
                    counter('iteration')
                    display_iterations()
                    main(mode)
                else:
                    display_iterations()
                    shutdown()
                    quit()

def main(method):
    worker(method)


def importdata():
    clear_screen()
    print('Enter previous run name (caps sensitive)')
    selectedfolder = input('#')
    print('Please Select an Option')
    print("(1) Run for x amount of TAGS gathered")
    print("(2) Run for x amount of iterations")
    userselectmode = input("# ")

    try:
        os.chdir(selectedfolder)
    except FileNotFoundError as err:
        print('Check previous run name and try again')
        time.sleep(3)
        importdata()
    with open('finalvideotags.json', 'r') as f:
        tags = json.load(f)
        parsedtags = parse_strlist(tags)
        for f in parsedtags:
            print(f)
            final_video_tags.append(f)
    with open('finished_video_urls.json', 'r') as f:
        urls = json.load(f)
        parsedurls = parse_strlist(urls)
        for f in parsedurls:
            print(f)
            finished_video_urls.append(f)
    with open('todo_urls.json', 'r') as f:
        turls = json.load(f)
        parsedturls = parse_strlist(turls)
        for f in parsedturls:
            print(f)
            todo_urls.append(f)
    os.chdir('../')
    print('Imported ' + str(len(parsedtags)) + ' total tags')
    print('Imported ' + str(len(parsedurls)) + ' finished videos')
    print('Imported ' + str(len(parsedturls)) + ' total todo urls')
    if userselectmode == '1':
        global usertagcount
        usertagcount = int(input('Enter amount of TAGS requested: '))
        global mode
        mode = 1
        main(mode)
    elif userselectmode == '2':
        global totaliterations
        totaliterations = int(input('Enter amount of ITERATIONS requested: '))
        global initial_video_url
        initial_video_url = todo_urls.pop()
        mode = 2
        main(mode)




def startQuestions():
        clear_screen()
        print('Please Select an Option')
        print("(1) Run for x amount of TAGS gathered")
        print("(2) Run for x amount of iterations")
        print("(3) Import previous data archive from another run")
        userselectmode = input("# ")
        if userselectmode == '1':
            global usertagcount
            usertagcount = int(input('Enter amount of TAGS requested: '))
            global mode
            mode = 1
            urlquestion()
            main(mode)
        elif userselectmode == '2':
            global totaliterations
            totaliterations = int(input('Enter amount of ITERATIONS requested: '))
            mode = 2
            urlquestion()
            main(mode)
        elif userselectmode == '3':
            importdata()
        else:
            print('Unknown selection')
            time.sleep(5)
            clear_screen()
            startQuestions()


startQuestions()
