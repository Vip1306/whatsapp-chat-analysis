import re
import pandas as pd
from urlextract import URLExtract
extractor = URLExtract()
def preprocess (data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    users = []
    messages = []
    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s',i)
        if entry[1:]:
            users.append(entry[1])
            messages.append(' '.join(entry[2:]))
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for i in df['hour']:
        if i == 23:
            period.append(str(i) + '-' + str('00'))
        elif i == 0:
            period.append(str('00') + '-' + str(i + 1))
        else:
            period.append(str(i) + '-' + str(i + 1))
    df['period'] = period
    return df


