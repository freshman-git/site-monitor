import sys
import urllib2
import smtplib
import time
########### Runtime Para ###########
url = 'http://www.google.com'
key = 'google'
type = 1 #0:disappear 1:appear
debug = False #not sending notification in debug mode
interval = 360 #secs - quick ref: 1hr: 3600
####################################
def notify(word):
    global url
    global key
    global debug
    ####### Private Settings #######
    gmail_smtp = 'smtp.gmail.com'
    gmail_username = 'gmail_user'
    gmail_password = 'gmail_pass'
    fr = 'gmail_user@gmail.com' #from
    to = ["gmail_user@gmail.com"] #to
    sub = url #subject
    b = 'Keyword \'' + key + '\' ' + word + ' on the site.' #message body
    msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (fr, ", ".join(to), sub, b)
    ###
    if debug:
        print ('[debug] sending ...\n' + msg)
    else:
        server = smtplib.SMTP(gmail_smtp, 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(gmail_username, gmail_password)
        server.sendmail(fr, to, msg)
        server.quit()
####################################
def check():
    global url
    global key
    global t
    sys.stdout.write('>')
    sys.stdout.flush()
    f = urllib2.urlopen(url)
    r = f.read() #response
    if key.lower() in r.lower():
        if debug:
            idx = r.lower().index(key.lower());
            print r[idx-100:idx+100]
        if type == 1:
            notify('appeared')
            return 1
    else:
        if debug:
            print r[0:200]
        if type == 0:
            notify('disappeared')
            return 1
    return 0
####################################

mark = '|'
wait = interval

while True:
    if wait >= interval:
        if check() == 1:
            exit()
        wait = 0
    else:
        wait += .5

    if mark == '|':
        mark = '-'
    else:
        mark = '|'
    sys.stdout.write(mark)
    sys.stdout.flush()
    time.sleep(.5)
    sys.stdout.write('\b')
    sys.stdout.flush()

    


