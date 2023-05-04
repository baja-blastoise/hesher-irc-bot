import socket
import time
from malookup import BANDLOOKUP, DISCOGLOOKUP, MEMBERLOOKUP, SIMILAR, ARTISTLOOKUP, ALBUMLOOKUP

with open('config.txt') as f:
    lines = f.readlines()

server = str()
channel = str()
botnick = str()
port = str()
bprint = []

for i in lines:
    if i.find('server') != -1:
        server = i.split('=')[-1].strip()
    if i.find('channel') != -1:
        channel = i.split('=')[-1].strip()
    if i.find('botnick') != -1:
        botnick = i.split('=')[-1].strip()
    if i.find('port') != -1:
        port = i.split('=')[-1].strip()
    if i.find('print') != -1:
        bread = i.split('=')[-1].strip()
        if bread == 'true':
            bprint = True
        if bread == 'false':
            bprint = False
    if i.find('command token') != -1:
        command_token = i.split('=')[-1].strip()

# create the socket object
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to: " + server)
irc.connect((server, int(port)))
irc.send(bytes("USER " + botnick + " " + botnick + " " +
         botnick + " :Metal Archives reference bot.\n", "UTF-8"))
irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
# claim registered nick - not setup serverside yet
irc.send(bytes("PRIVMSG nickserv :iNOOPE\r\n", "UTF-8"))

# try to read in help message
try:
    helpmsg = 1
    with open('help.txt') as f:
        lines = f.readlines()
except Exception as e:
    helpmsg = 0
    print("Could not find help.txt in this folder.")
    print(e)

onetime = 0
while 1:
    try:
        text = irc.recv(2040).decode("UTF-8")
    except Exception as e:
        text = 'failed to decode'
        print(e)
    # print(text)  # silence this later to keep output cleanish on releas)e

    # respond to PING request from server - best not to touch this
    if text.find('PING') != -1:
        irc.send(bytes('PONG ' + text.split()[1] + '\r\n', "UTF-8"))
        if onetime == 0:
            onetime = 1
            irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
        elif onetime == 1:
            onetime = 2

    # help message - text file should be read in on startup
    elif text.find(':!help') != -1:
        print('!help command found')
        print(text)
        if helpmsg == 1:
            for i in lines:
                irc.send(bytes('PRIVMSG ' + channel + ' ' + i + '\r\n', "UTF-8"))
        else:
            irc.send(bytes('PRIVMSG ' + channel +
                     ' No help.txt found ' + '\r\n', "UTF-8"))

    # find basic band information
    elif text.find(':!band ') != -1:
        print('!band command found')
        print(text)
        t0 = time.time()
        # handles band numbers for disambiguation
        if text.find('|') != -1:
            text = text.split('|')
            bandnumber = text[-1]
            text = text[0].split(':!band')
            bandname = text[-1].strip()
            print('Band name: ' + bandname)
            print('Band number: ' + str(bandnumber))
            results = BANDLOOKUP(bandname, bandnumber, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!band')
            bandname = t[-1].strip()
            print(bandname)
            results = BANDLOOKUP(bandname, 0, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        t1 = time.time()
        print(t1-t0)

    # lookup discography
    elif text.find(':!discog ') != -1:
        print('!discog command found')
        print(text)
        t0 = time.time()
        # get discog type first
        if text.find(',') != -1:
            disctype = text.split(',')[-1].strip()
            text = text.split(',')[0]
        else:
            disctype = 'main'
        # handles band numbers for disambiguation
        if text.find('|') != -1:
            text = text.split('|')
            bandnumber = text[-1]
            text = text[0].split(':!discog')
            bandname = text[-1].strip()
            print('Band name: ' + bandname)
            print('Band number: ' + str(bandnumber))
            print('Type: ' + disctype)
            results = DISCOGLOOKUP(bandname, bandnumber, disctype, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!discog')
            bandname = t[-1].strip()
            print('Band name: ' + bandname)
            print('Type: ' + disctype)
            results = DISCOGLOOKUP(bandname, 0, disctype, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        t1 = time.time()
        print(t1-t0)

    # lookup band membership
    elif text.find(':!members ') != -1:
        print('!members commmand found')
        print(text)
        t0 = time.time()
        # get membership type first - default to either 'Active' or 'last Known'
        if text.find(',') != -1:
            membertype = text.split(',')[-1].strip()
            text = text.split(',')[0]
        else:
            membertype = 'Current'
        # handles band numbers for disambiguation
        if text.find('|') != -1:
            text = text.split('|')
            bandnumber = text[-1]
            text = text[0].split(':!members')
            bandname = text[-1].strip()
            print('Band name: ' + bandname)
            print('Band number: ' + str(bandnumber))
            print('Type: ' + membertype)
            results = MEMBERLOOKUP(bandname, bandnumber, membertype, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!members')
            bandname = t[-1].strip()
            print('Band name: ' + bandname)
            print('Type: ' + membertype)
            results = MEMBERLOOKUP(bandname, 0, membertype, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        t1 = time.time()
        print(t1-t0)

    # find similar band information
    elif text.find(':!similar ') != -1:
        print('!similar command found')
        print(text)
        t0 = time.time()
        # band number for disambiguation
        if text.find('|') != -1:
            text = text.split('|')
            bandnumber = text[-1]
            text = text[0].split(':!similar')
            bandname = text[-1].strip()
            print('Band name: ' + bandname)
            print('Band number: ' + str(bandnumber))
            results = SIMILAR(bandname, bandnumber, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!similar')
            bandname = t[-1].strip()
            print('Band name: ' + bandname)
            results = SIMILAR(bandname, 0, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))

    # artist lookup
    elif text.find(':!artist ') != -1:
        print('!artist command found')
        print(text)
        to = time.time()
        # artist number for disambiguation?  might come later
        if text.find('|') != -1:
            text = text.split('|')
            artistnumber = text[-1]
            text = text[0].split(':!artist')
            artistname = text[-1].strip()
            print('Artist name: ' + artistname)
            print('Artist number: ' + str(artistnumber))
            results = ARTISTLOOKUP(artistname, artistnumber, bprint)
            if results.find('\n'):
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!artist')
            artistname = t[-1].strip()
            artistnumber = 0
            print('Artist name: ' + artistname)
            results = ARTISTLOOKUP(artistname, artistnumber, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))

    # album lookup
    elif text.find(':!album ') != -1:
        print('!album command found')
        print(text)
        t0 = time.time()
        # album number for disambiguation?  might come later
        if text.find('|') != -1:
            text = text.split('|')
            albumnumber = text[-1].strip()
            text = text[0].split(':!album')
            text2 = text[-1].split('!album')[-1].strip().split(':')
            albumname = text2[-1].strip()
            bandname = text2[0].strip()
            print('Album Name: ' + albumname)
            print('Band Name: ' + bandname)
            print('Album number: ' + albumnumber)
            results = ALBUMLOOKUP(bandname, albumname, albumnumber, bprint)
            if results.find('\n'):
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
        else:
            t = text.split(':!album')
            text2 = text.split('!album')[-1].strip().split(':')
            bandname = text2[0].strip()
            albumname = text2[-1].strip()
            print('Album Name: ' + albumname)
            print('Band Name: ' + bandname)
            albumnumber = 0
            results = ALBUMLOOKUP(bandname, albumname, albumnumber, bprint)
            if results.find('\n') != -1:
                results = results.split('\n')
                for i in results:
                    irc.send(bytes('PRIVMSG ' + channel +
                             ' ' + i + '\r\n', "UTF-8"))
            else:
                irc.send(bytes('PRIVMSG ' + channel +
                         ' ' + results + '\r\n', "UTF-8"))
