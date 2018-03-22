import numpy as np
import pandas as pd
import seaborn as sns

def spam(mail):
    emails = pd.read_csv('./spam.csv', header=None, names=['term', 'hardcap','softcap', 'occurs'])
    #print(emails)
    f = mail
    terms = emails['term'].tolist()

    for line in f:
        line = line.rstrip()
        if line in terms:
            data = emails.loc[emails.term == line]
            data['occurs'] = data['occurs'].apply(lambda x: x+1)
            #data = data.set_index('term')
            data['hardcap'][data['occurs'] == (data['softcap'] + 3)] = +1
            data['softcap'][data['occurs'] == 5] = +1
            spamcount = data['hardcap'].sum()
            emails.update(data)
            emails.to_csv('spam.csv')
    return emails, spamcount

