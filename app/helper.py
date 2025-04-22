import re
from collections import Counter
import pandas as pd
import numpy as np
from urlextract import URLExtract
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
from wordcloud import WordCloud
import emoji
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def preprocess_chat(text:str) -> pd.DataFrame:
    """
    Preprocesses raw WhatsApp chat export text and returns a cleaned DataFrame with structured data.

    Parameters:
    -----------
    text : str
        The raw text from a WhatsApp chat export file.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing structured chat data with the following columns:
        - 'date': Timestamp of the message.
        - 'user': Sender of the message.
        - 'message': Message content.
        - 'year': Year extracted from the timestamp.
        - 'month': Month extracted from the timestamp.
        - 'day': Day of the week extracted from the timestamp.
        - 'hour': Hour extracted from the timestamp.
        - 'minute': Minute extracted from the timestamp.
    """
    global df
    
    # Define regex pattern to extract date and time at the beginning of each message
    pattern = r'\d+/\d+/\d+,\s\d+:\d+\W*\w*\s- '
    messages = re.split(pattern,text)[1:]           # Split messages based on the pattern and discard the first empty element
    dates = re.findall(pattern,text)                # Extract all date-time strings that match the pattern

    df = pd.DataFrame({'date':dates,'content':messages})   # Create a DataFrame with extracted dates and messages
    
    df = df[df.content.str.contains(':')]            # Filter out system messages (those without a colon to indicate user-message format)
    df[['user','message']]=df['content'].str.strip().str.split(':',n=1,expand=True)
    df.message = df.message.str.strip()
    df.drop(columns='content',inplace=True)

    # Clean and convert date strings to datetime format
    df['date'] = pd.to_datetime(df.date.str.rstrip(' - '), dayfirst=True, errors='coerce' )
    df.dropna(subset=['date'], inplace=True)

    # Extract date and time components for analysis
    df['year'] = df.date.dt.year
    df['month'] = df.date.dt.month
    df['day'] = df.date.dt.day_name()
    df['hour'] = df.date.dt.hour
    df['minute'] = df.date.dt.minute

    return df

def fetch_stats(selected_user:str)->tuple :
    """
    Fetches chat statistics for a selected user or for the entire chat.

    Parameters:
    -----------
    selected_user : str | None
        Username to filter data by. If None, stats are calculated for all users.

    Returns:
    --------
    tuple[int, int, int, int, int, int]
        A tuple containing:
        - Total number of messages sent
        - Total number of words
        - Total number of media files shared
        - Total number of links shared
        - Total number of deleted messages
        - Total number of emojis used
    """

    global data, words_list, emojis_list

    # Filter the DataFrame for the selected user, or use the whole dataset
    data = df if selected_user == None else df[df['user'] == selected_user]
    total_messages_sent = data.shape[0]
    
    extractor = URLExtract()
    
    words_list, links_list, emojis_list = [], [], [] 
    media_shared, deleted_messages = 0, 0

    # Iterate through each message to compute stats
    for message in data.message:
        if message =='<Media omitted>':
            media_shared+=1
        elif message == 'This message was deleted':
            deleted_messages+=1
        else :
            # Separate out emojis and clean message
            cleaned_message = ''.join([char for char in message if not emoji.is_emoji(char)])
        
            emojis_list.extend([char for char in message if emoji.is_emoji(char)])

            # Add words (excluding emojis and links)
            words_list.extend(cleaned_message.split())
            # Extract and count links
            links = extractor.find_urls(cleaned_message)
            
            if links:
                links_list.extend(links)
                for link in links:
                        words_list.remove(link) 
    
    total_words = len(words_list)
    total_links = len(links_list)
    total_emojis = len(emojis_list)
    
    return total_messages_sent, total_words, media_shared, total_links, deleted_messages, total_emojis


def get_active_users_chart()->Figure:
    """
    Displays a horizontal bar chart of the most active users in the chat.

    The function calculates the percentage of messages sent by each user,
    identifies the top 6 most active users, and visualizes their engagement
    using a bar plot.

    Returns:
    --------
    None
    """ 
    # Calculate percentage of messages per user
    active_users = np.round((df.user.value_counts()/df.shape[0])*100,2).head(6)
    
    fig,ax = plt.subplots(figsize=(8,5))
    sns.set_style('darkgrid')
    
    x,y = active_users.values, active_users.index
    plot = sns.barplot(x=x, y=y, palette="viridis")

    # Annotate bars with percentage values
    for i, v in enumerate(x):
        plot.text(v + 1, i, str(v)+'%', color='black', va='center')

    # Clean up plot appearance
    ax.set_ylabel("") 
    plt.xticks([])
    sns.despine(top=False,right=False)
    # sns.despine(left=True, bottom=True)
    plt.tight_layout()
    return fig    


def remove_stopwords(words: list[str]) -> list[str]:
    """
    Removes common English stopwords from a list of words.

    Parameters:
    -----------
    words : list[str]
        The list of words to filter.

    Returns:
    --------
    list[str]
        Filtered list without stopwords.
    """
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    return filtered_words

    
def create_wordcloud()->Figure:
    """
    Generates and displays a word cloud from the global `words_list`.

    The function uses the WordCloud library to visualize the most frequent words
    from the list `words_list`, which should contain cleaned and tokenized words
    from chat messages.

    Returns:
    --------
    None
    """
    global words_list
    # Create a WordCloud object with specified dimensions and settings
    wc_fig = WordCloud(width=500,height=500,min_font_size=10,background_color='white',max_words=100)
    words_list = remove_stopwords(words_list)
    # Display the word cloud using matplotlib
    wc_fig.generate(' '.join(words_list))
    fig = plt.figure()
    plt.imshow(wc_fig) 
    plt.axis('off')
    return fig

    
def get_most_common_words(n:int=10)->Figure:
    """
    Plots a bar chart of the most common words in the global `words_list`.

    Parameters:
    -----------
    n : int, optional (default=10)
        The number of top words to display in the chart.

    Returns:
    --------
    None
    """
    global words_list
    words_list = remove_stopwords(words_list)
    # Count the n most common words in the list
    most_common_words = pd.DataFrame(Counter(words_list).most_common(n))
    fig, ax = plt.subplots(figsize=(8,8))
    sns.set_style('dark')
    
    plot = sns.barplot(data=most_common_words, x=1, y=0, palette="rocket")
    
    plt.title('Most Used words', pad=20, fontsize=14, fontweight='bold')
    plt.xlabel('Count', labelpad=10)
    plt.ylabel('Words', labelpad=10)
        
    return fig


def get_most_used_emoji()-> pd.DataFrame:
    """
    Returns a DataFrame of the top 10 most frequently used emojis 
    from the global `emojis_list`.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with two columns:
        - 'emoji': The emoji character
        - 'count': Number of times the emoji was used
    """
    emoji_df = pd.DataFrame(Counter(emojis_list).most_common(10),columns=['emoji','count'])
    return emoji_df    


def get_timeline_graphs()->tuple:

    year_stat = data.groupby(['year','month']).message.count().reset_index()
    year_stat.month = year_stat.month.map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',\
                     8:'August',9:'September',10:'october',11:'November',12:'December'})
    year_stat['index'] = year_stat['month']+'-'+year_stat['year'].astype(str)
    year_stat.set_index('index',inplace=True)
    
    date_stat = data.groupby(data.date.dt.date).message.count()
    
    week_stat = data.groupby(data.date.dt.weekday).message.count().sort_index()
    week_stat.index = week_stat.index.map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})

    month_stat = data.groupby(data.date.dt.month).message.count().sort_index()
    month_stat.index = month_stat.index.map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',\
                     8:'August',9:'September',10:'october',11:'November',12:'December'})


    hour_stat = pd.pivot_table(data=data,columns='hour',index='day',values='message',aggfunc= 'count',fill_value=0)
    new_time = [str(i)+'-'+'00'  if i==23 else str(i)+'-'+str(i+1) for i in hour_stat.columns]
    hour_stat.columns = new_time

    return year_stat, date_stat, week_stat, month_stat, hour_stat