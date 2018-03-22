#!/usr/bin/env python

import sys
import imaplib
import email
import email.header
import getpass
import datetime
from bs4 import BeautifulSoup
import re
from OpenSSL import SSL
EMAIL_ACCOUNT = "listerd37@gmail.com"
PASSWD = "Reddwarf"
USR1 = "David"
USR2 = "Lister"
M = imaplib.IMAP4_SSL('imap.gmail.com',993)
def process_mailbox():
    rv, data = M.search(None, "ALL")
    #resp, items = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data, = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        if msg.is_multipart():
            for part in msg.get_payload():
                body = part.get_payload()
        subject = str(hdr).encode("utf-8")
        print('Message %s: %s' % (num, subject))
        print('Body:', body)
        soup = BeautifulSoup(body, "lxml")
        images = []
        links = []
        links2 = []
        imgCount = 0
        linkCount = 0
        attCount = 0
        wordCount = 0
        for img in soup.findAll('img'):
            images.append(img.get('src'))
            if '//0' in images:
                print('suspicious image found')
                imgCount = imgCount + 2
            if 'width = 0' in images:
                print('suspicious image found')
                imgCount = imgCount + 1
            if 'height = 0' in images:
                print('suspicious image found')
                imgCount = imgCount + 1
        print('images found: ', images)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part == ".exe":
                print('suspicious attatchment, do not open!')
            if part == ".apk":
                print('suspicious attatchment, do not open!')
            if part == ".ipa":
                print('suspicious attatchment, do not open!')
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
        print("links found", links)
        
try:
    rv, data = M.login(EMAIL_ACCOUNT, PASSWD)
except imaplib.IMAP4.error:
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select("INBOX")
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox()
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()