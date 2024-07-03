import streamlit as st
import pandas as pd
import re
import helper
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns


if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
    
st.set_page_config(page_title='whatsapp chat analyzer',layout='wide',initial_sidebar_state=st.session_state.sidebar_state)
_,head,_=st.columns(3)
with head:
    st.title('Chat analyser',anchor=False)

file=st.sidebar.file_uploader('Upload')

def sidebar_change():
        st.session_state.sidebar_state='collapsed'
if file:
    data=file.getvalue().decode('utf-8')
    df=helper.data_process(data)
    users_list=df['user'].unique()
    with st.sidebar.form("my_form"):
        selected_user=st.selectbox('Select User',options=users_list,placeholder='over all',index=None)
        click=st.form_submit_button('Show analysis',on_click=sidebar_change)
    if click:
        left,right=st.columns(2)
        with left:
            col1,col2=st.columns(2)
            stats=helper.fetch_stats(selected_user)
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
        with right:
            with st.container(border=True):
                st.header('Users Interaction',anchor=False)
                x=helper.active_user()
                fig,ax=plt.subplots()
                ax.barh(x.index,x.values)
                for i in ax.containers:
                    ax.bar_label(i,fmt='{}%') 
                plt.xticks([])
                st.pyplot(fig)
        word,emoji=st.columns([8,2])
        with word:
            with st.container(border=True):
                st.header('Common used words',anchor=False)
                l,r=st.columns(2,gap='large')
                with r:
                    img=helper.wrd_cld(selected_user)
                    fig=plt.figure(figsize=(4,2))
                    plt.imshow(img) 
                    plt.axis('off')
                    st.pyplot(fig,use_container_width=False)
                with l:
                    mc_df=helper.common_words()
                    fig,ax=plt.subplots()
                    ax.barh(mc_df[0],mc_df[1])
                    ax.invert_yaxis()
                    st.pyplot(fig)
        with emoji:
            with st.container(border=True):
                st.subheader('Used Emojis',anchor=False)
                em_df=helper.emoji_stat(selected_user)
                fig,ax=plt.subplots()
                ax.bar(height=em_df['count'],x=em_df['emoji'])
                st.dataframe(em_df,hide_index=True)
        with st.container(border=True):
            st.title('Timeline',anchor=False)
            left,right=st.columns(2,gap='large')
            with left:
                st.write(' ')
                st.subheader('Overall activity')
                monthly,daily,week,mbar,pi=helper.get_timeline(selected_user)
                fig,ax=plt.subplots()
                ax.plot(monthly.index,monthly.message)
                plt.xticks(rotation=90) 
                plt.yticks([]) 
                st.pyplot(fig)
            with right:
                st.write(' ')
                st.subheader('Daily activity')
                fig,ax=plt.subplots()
                ax.plot(daily)
                plt.xticks(rotation=90)
                ax.set_ylabel('activity')
                plt.yticks([])  
                st.pyplot(fig)
            with left:
                st.write(' ')
                st.subheader('weekdays activity')
                fig,ax=plt.subplots()
                week.plot.barh()
                plt.xticks(rotation=90)  
                st.pyplot(fig)
            with right:
                st.write(' ')
                st.subheader('Monthly activity')
                fig,ax=plt.subplots()
                mbar.plot.barh()
                plt.xticks(rotation=90)  
                st.pyplot(fig)

            fig,ax=plt.subplots()
            st.write(' ')
            st.subheader('Hourly activity')
            sns.heatmap(pi,cmap='plasma',linewidths=.1)
            plt.ylabel('') 
            st.pyplot(fig)


    
    
