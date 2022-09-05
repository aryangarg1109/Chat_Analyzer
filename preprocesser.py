import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    #Creating Dataframe
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    #covert message_date_type
    df['message_date']=pd.to_datetime(df['message_date'],format='%m/%d/%y, %H:%M %p - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    users=[]
    messages=[]
    for mess in df['user_message']:
         entry = re.split('([\w\W]+?):\s', mess)
       
         if entry[1:]:
             users.append(entry[1])
             messages.append(entry[2])
         else:
             users.append('group_notification')
             messages.append(entry[0])
    df['users']=users
    df['message']=messages
    df.drop(columns=['user_message'], inplace=True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hours']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    
    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 11:
            period.append(str(hour) + "-" + str('12'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    return df
