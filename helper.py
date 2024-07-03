import pandas as pd
import re,numpy as np
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter   
import emoji
import seaborn as sns

extractor=URLExtract()

def data_process(data):
    pattern=r'\d+/\d+/\d+,\s\d+:\d+\W*\w*\s-'
    msg=re.split(pattern,data)[1:]
    date=re.findall(pattern,data)
    global df
    df=pd.DataFrame({'date':date,'content':msg})
    df=df[df.content.str.contains(':')]
    df[['user','message']]=df['content'].str.strip().str.split(':',n=1,expand=True)
    df.message=df.message.str.strip()
    df.drop(columns='content',inplace=True)
    df['date']=pd.to_datetime(df.date.str.rstrip('-'),dayfirst=True)
    df['year']=df.date.dt.year
    df['month']=df.date.dt.month
    df['day']=df.date.dt.day_name()
    df['hour']=df.date.dt.hour
    df['minute']=df.date.dt.minute
    return df


def fetch_stats(selected_user):
    dff=df if selected_user==None else df[df['user']==selected_user]
    n_message=dff.shape[0]
    global words
    words=[]
    links=[]
    media=0
    for i in dff.message:
        if not (i.count('*')>6 and len(extractor.find_urls(i))>1):
            if i!='<Media omitted>':
                words.extend(i.split())
            else:
                media+=1
        links.extend(extractor.find_urls(i))   
    n_words=len(words)
    n_links=len(links)

    words=[i.lower() for i in words]
    del_msg=dff[dff.message=='This message was deleted'].shape[0]
    return n_message,n_words,media,n_links,del_msg

def active_user():
    x=np.round((df.user.value_counts()/df.shape[0])*100,2).head(6)
    return x

def wrd_cld(selected_user):
    dff=df if selected_user==None else df[df['user']==selected_user]
    dff=dff[dff.message!='<Media omitted>']
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    return wc.generate(dff.message.str.cat(sep=' '))

def common_words():
    return pd.DataFrame(Counter(words).most_common(10))

def emoji_stat(selected_user):
    dff=df if selected_user==None else df[df['user']==selected_user]
    emojis=[]
    for i in dff.message:
        emojis.extend([c for c in i if emoji.is_emoji(c)])
    return pd.DataFrame(Counter(emojis).most_common(10),columns=['emoji','count'])

def get_timeline(selected_user):
    dff=df if selected_user==None else df[df['user']==selected_user]
    m=dff.groupby(['year','month']).message.count().reset_index()
    m.month=m.month.map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',\
                     8:'August',9:'September',10:'october',11:'November',12:'December'})
    m['index']=m['month']+'-'+m['year'].astype(str)
    m.set_index('index',inplace=True)
    
    d=dff.groupby(dff.date.dt.date).message.count()
    
    w=dff.groupby(dff.date.dt.weekday).message.count().sort_index()
    w.index=w.index.map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})

    mb=dff.groupby(dff.date.dt.month).message.count().sort_index()
    mb.index=mb.index.map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',\
                     8:'August',9:'September',10:'october',11:'November',12:'December'})


    pi=pd.pivot_table(data=dff,columns='hour',index='day',values='message',aggfunc= 'count',fill_value=0)
    new_time=[]
    for i in pi.columns:
        if i==23:
            new_time.append(str(i)+'-'+'00')
        else:
            new_time.append(str(i)+'-'+str(i+1))
    pi.columns=new_time
    

    return m,d,w,mb,pi

    





