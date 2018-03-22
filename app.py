from flask import Flask, render_template, jsonify, request
from imapclient import IMAPClient
import json
import simplejson
import email
import email.header
import imaplib
import numpy as np
from itertools import cycle, islice
from spamcounter import spam
import base64
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')
    
@app.route('/m')
def m():
    server = IMAPClient('imap.gmail.com', use_uid=True)
    server.login('listerd37@gmail.com', 'Reddwarf')
    select_info = server.select_folder('[Gmail]/All Mail')
    messages = server.search()
    mail = []
    id = []
    spam = []
    mailbody = []
    mailbody2 = []
    for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
        envelope = data[b'ENVELOPE']
        id.append(msgid)
        subject = envelope.subject.decode('utf-8')
        sub = decode_mime_words(subject)
        mail.append(sub)
    con=imaplib.IMAP4_SSL('imap.gmail.com')
    con.login('listerd37@gmail.com','Reddwarf')
    con.list()
    con.select("INBOX")
    rv, data = con.search(None, "ALL")
    for num in data[0].split():
        result,data=con.fetch(num, '(RFC822)')
        raw=email.message_from_bytes(data[0][1])
        body = ""
        if raw.is_multipart():
            for payload in raw.walk():
                if payload.get_content_type() == 'text/plain':
                    mailbody.append(payload.get_payload(None, True))
        else:
            mailbody.append(raw.get_payload())
    return simplejson.dumps({"mail": mail, "body": mailbody})

def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))
    return decode_mime_words(u'=?utf-8?Q?Subject=c3=a4?=X=?utf-8?Q?=c3=bc?=')

if __name__ == '__main__':
	app.run(use_reloader=True, debug=True)