# Standard and third-party imports
import io
import zipfile
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Custom helper module containing preprocessing and analytics functions
import helper

# Function to collapse the sidebar after form submission
def sidebar_change():
        st.session_state.sidebar_state = 'collapsed'

# Initialize sidebar state if not already set
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# Set the Streamlit page configuration
st.set_page_config(page_title='Chat Trakr',layout='wide',initial_sidebar_state=st.session_state.sidebar_state)

# Display title in the center column of a 3-column layout
_, title, _=st.columns(3)
with title:
    st.title('Chat Analysis',anchor=False)

st.sidebar.title("Chat Trakr",anchor=False)
file = st.sidebar.file_uploader('Upload')    

# Process the uploaded file if present
if file:
    # Read and unzip the uploaded chat file
    bytes_data = file.getvalue()
    with zipfile.ZipFile(io.BytesIO(bytes_data)) as zip_ref:  
        text_file = zip_ref.namelist()[0]
        with zip_ref.open(text_file) as file:
            text = file.read().decode('utf-8')

    # Preprocess chat data using helper function
    df = helper.preprocess_chat(text)
    users_list = df.user.unique()

     # Sidebar form to select user and trigger analysis
    with st.sidebar.form("my_form"):
        selected_user = st.selectbox('Select User', options=users_list, placeholder='over all', index=None)
        click = st.form_submit_button('Show analysis', on_click=sidebar_change)

    # Display analytics only if "Show analysis" button is clicked        
    if click:
        left,right = st.columns(2)
        
        with left:
            col1, col2 = st.columns(2)
            stats = helper.fetch_stats(selected_user)

            # Show stats: Total messages, words, media, links, deleted messages, emojis
            with col1:
                with st.container(border=True):
                    st.subheader('Total Messages',anchor=False)
                    st.subheader(stats[0],anchor=False)
            with col2:
                with st.container(border=True):
                    st.subheader('Total Words',anchor=False)
                    st.subheader(stats[1],anchor=False)
            with col1:
                with st.container(border=True):
                    st.subheader('Media shared',anchor=False)
                    st.subheader(stats[2],anchor=False)  
            with col2:
                with st.container(border=True):
                    st.subheader('Links shared',anchor=False)
                    st.subheader(stats[3],anchor=False)
            with col1:
                with st.container(border=True):
                    st.subheader    ('Deleted messages',anchor=False)
                    st.subheader(stats[4],anchor=False)
            with col2:
                with st.container(border=True):
                    st.subheader('Emojis shared',anchor=False)
                    st.subheader(stats[5],anchor=False)                    
        
        # Display active users chart in right column
        with right:
            with st.container(border=True):
                st.header('Users Interaction',anchor=False)
                active_users_chart = helper.get_active_users_chart()
                st.pyplot(active_users_chart)

        # Section for common words and emoji usage
        words_sec, emojis_sec = st.columns([8,2])
        with words_sec:
            with st.container(border=True):
                st.header('Common used words',anchor=False)
                left,right = st.columns(2,gap='large')
                with right:
                    fig = helper.create_wordcloud()
                    st.pyplot(fig)
                    
                with left:
                    common_words_fig = helper.get_most_common_words()
                    st.pyplot(common_words_fig)

        with emojis_sec:
            with st.container(border=True):
                emoji_df = helper.get_most_used_emoji()
                st.subheader("Used Emojis",anchor=False)
                st.dataframe(emoji_df,hide_index=True)

        # Timeline and activity plots
        with st.container(border=True):
            st.title('Timeline',anchor=False)
            left,right = st.columns(2,gap='large')
            
            year_stat, date_stat, week_stat, month_stat, hour_stat = helper.get_timeline_graphs()
            with left:
                st.subheader('Overall Activity',anchor=False)
                fig,ax = plt.subplots()
                sns.lineplot(data = year_stat, y='message', x='index', markers='o', dashes=False)
                
                plt.xticks(rotation=90)
                plt.yticks([]) 
                plt.grid(True)
                ax.set_xlabel('')
                ax.set_ylabel('Interaction')

                st.pyplot(fig)

            with right :
                st.subheader('Monthly Activity',anchor=False)
                fig,ax = plt.subplots()
                sns.barplot(data = month_stat.reset_index(), x='message', y='date', palette='mako')
                
                plt.xticks([])
                plt.grid(True)
                ax.set_xlabel('')
                # ax.set_ylabel('Interaction')

                st.pyplot(fig)

            with left :
                st.subheader('Weekdays Activity',anchor=False)
                fig,ax = plt.subplots()
                sns.barplot(data = week_stat.reset_index(), x='message', y='date', palette='crest')
                
                plt.xticks([])
                plt.grid(True)
                ax.set_xlabel('')
                # ax.set_ylabel('Interaction')

                st.pyplot(fig)

            with right :
                st.subheader('Daily Activity',anchor=False)
                fig,ax = plt.subplots()
                sns.lineplot(date_stat)
                
                plt.xticks(rotation=90)
                plt.yticks([]) 
                plt.grid(True)
                ax.set_xlabel('')
                ax.set_ylabel('Interaction')

                st.pyplot(fig)

            fig,ax = plt.subplots(figsize=(10,4))
            st.subheader('Hourly activity')
            sns.heatmap(hour_stat,cmap='flare',linewidths=.1)
            plt.xlabel('Hours') 
            plt.ylabel('') 
            st.pyplot(fig,use_container_width=False)
                 