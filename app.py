import streamlit as st
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import emoji
import numpy as np
import seaborn as sns
st.sidebar.title('whatsapp chat analysis')
uploaded_file = st.sidebar.file_uploader('choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user = st.sidebar.selectbox('show analysis wrt',user_list)
    if st.sidebar.button('Show analysis'):
        num_messages, words, num_media_messages,links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistical Whatsapp Chat')
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric('Total messages',num_messages)
        with col2:
            st.metric('Total words', words)
        with col3:
            st.metric('Media_shared', num_media_messages)
        with col4:
            st.metric('Links_shared', links)
    if selected_user == 'overall':
        st.title('Most Busy Users')
        x,new_df = helper.most_busy_users(df)
        fig,ax = plt.subplots()
        col1,col2 = st.columns(2)
        with col1:
            ax.bar(x.index,x.values,color = 'red')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    most_common_df = helper.most_common_words(selected_user,df)
    st.title('Most Common Words')
    st.dataframe(most_common_df)
    fig,ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1],color = 'orange')
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)
    st.title('Emoji Analysis')
    emoji_df=helper.emoji_helper(selected_user, df)
    col1,col2 = st.columns(2)
    fig,ax=plt.subplots()
    with col1:
        st.dataframe(emoji_df)
    with col2:
        ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct = '%0.1f%%')
        st.pyplot(fig)
    st.title('Month Timeline Analysis')
    timeline=helper.monthly_timeline(selected_user, df)
    fig,ax=plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.title('Daily Timeline Analysis')
    daily_timeline=helper.daily_timeline_helper(selected_user, df)
    fig,ax=plt.subplots()
    ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='purple')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.title('Activity Map')
    busy_day=helper.most_busy_days(selected_user, df)
    fig,ax=plt.subplots()
    col1,col2=st.columns(2)
    with col1:
        st.header('Most Busy Days')
        st.dataframe(busy_day)
        ax.bar(busy_day['day_name'], busy_day['count'], color='blue')
        plt.xticks(rotation='vertical',fontsize=20)
        plt.yticks(fontsize=20)
        st.pyplot(fig)
    busy_month = helper.most_busy_months(selected_user, df)
    fig,ax=plt.subplots()
    with col2:
        st.header('Most Busy Months')
        st.dataframe(busy_month)
        ax.bar(busy_month['month'], busy_month['count'], color='green')
        plt.xticks(rotation='vertical',fontsize=20)
        plt.yticks(rotation='vertical',fontsize=20)
        st.pyplot(fig)
    st.title('Online Activity Map')
    user_heatmap=helper.activity_heatmap(selected_user, df)
    fig,ax=plt.subplots()
    ax=sns.heatmap(user_heatmap)
    st.pyplot(fig)
