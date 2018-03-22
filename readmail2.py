from imapclient import IMAPClient
import email
import imaplib
from bs4 import BeautifulSoup
import re
user = 'xxxxxxx@gmail.com'
password = 'xxxxxx'
server = IMAPClient('imap.gmail.com', use_uid=True)
server.login(user,password)
select_info = server.select_folder('INBOX')
print('%d messages in INBOX' % select_info[b'EXISTS'])
messages = server.search()
print("%d messages" % len(messages))
con=imaplib.IMAP4_SSL('imap.gmail.com')
con.login(user,password)
con.list()
con.select("INBOX")
rv, data = con.search(None, "ALL")

for num in data[0].split():
    result,data=con.fetch(num, '(RFC822)')
    raw=email.message_from_bytes(data[0][1])
    body = ""
    if raw.is_multipart():
        for payload in raw.get_payload():
                body = payload.get_payload(None, True)
                fr = raw['from']
                print(fr)
    else:
        body = raw.get_payload()
    print(body)
    
for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
    envelope = data[b'ENVELOPE']
    m = [msgid, envelope.subject.decode()]
server.logout()

