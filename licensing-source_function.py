# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 11:12:37 2023

@author: HaroonIqbal
"""



"""
This script scraps data from the variable url and gives us the following information :
    title, title link, author, text, image, service_name, service_icon, approver
    



@author: HaroonIqbal
The Insights Family

===========================Version Control====================================
Number=========================Author=======================Notes=============
V1                              HI                   Initial Release
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import configparser
import mysql.connector
from datetime import datetime,timezone
from pprint import pprint 


# connection to database
config = configparser.ConfigParser()
#config.read(r'C:/Users/Haroon/Documents/config.txt')
#config.read(r'/home/portaladmin/scripts/python/Data_Science/config')
config.read(r'/home/roohihea/scripts/projects/config')
mysqlhost  = config.get('DEFAULT','mysqlhost')
mysqldatabase = config.get('DEFAULT','mysqldatabase')
mysqlusername  = config.get('DEFAULT','mysqlusername')
mysqlpassword  = config.get('DEFAULT','mysqlpassword')

db = mysql.connector.connect(
    host = mysqlhost,
    database = mysqldatabase,
    user = mysqlusername,
    password = mysqlpassword 
)

cur = db.cursor()
now = datetime.now()


cur = db.cursor()
now = datetime.now()


# dd/mm/YY H:M:S
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

base_url = 'https://www.licensingsource.net/'
url = 'https://www.licensingsource.net/news/'
icon_image = 'https://www.licensingsource.net/wp-content/uploads/2016/10/favicon1.png'
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')

code = data.text

def get_urls(soup):
    """
    

    Parameters
    ----------
    soup :  TYPE class 'bs4.BeautifulSoup
        The parameter passes the html code to the function 


    Returns
    -------
    urls : List
       This variable  returns the list of website found on the url passed through the soup variable

    """
    urls = []
    data_web = soup.findAll('div',attrs={'class':'page-content'})
    for div in data_web:
        links = div.findAll('a')
        for a in links:
         
            links = a.get('href')
            urls.append(links)
    urls = list(dict.fromkeys(urls))
    return urls




def scrap_website(urls):
    """
    

    Parameters
    ----------
    urls : List
         This variable  returns the list of website found on the url passed through the soup variable which we will scrap.

    Returns
    -------
    my_data :  dictionary
        My_data will give us all the data that we scrapped in a dictionary format for each website

    """
    my_data = []
    
    for i in urls:
        
        if i.startswith (base_url) and '/jobs/' not in i:
           
           
            data1 = requests.get(i)
            html = BeautifulSoup(data1.text, 'html.parser')
            title_tag = html.find("meta", attrs={'property': 'og:title'})
            title =title_tag['content']
            description_meta = html.find("meta", attrs={'property': 'og:description'})
            description =description_meta['content']
            image_meta = html.find("meta", attrs={'property': 'og:image'})
            images_url =image_meta['content']
          
            data_web = html.find('div',attrs={'class':'postauthors'})
            
            date_span = data_web.find('span')
            post_date = date_span.text.strip()
            
            date_span.extract()
            author = data_web.text.strip()
            author = author[3:]
            #my_data.append({'title' :title,'description':description,'date':date,'author':author,'images':images_url,'weblink':i})
            my_data.append({'title':title,'title_link':str(i),'author':author,'text':description,'image':images_url,'service_name':'licensingsource.net','service_icon':icon_image,'approved':'Y'})
    
   
    return my_data



def list_to_df(my_data):
    """
    

    Parameters
    ----------
    my_data : Dictionary
        My_data is the dictionary we created in the previous function which we will convert into a DataFrame and 
        convert the timestamp_readble column in general datetime format.

    Returns
    -------
    licensing_source_df : DF
        we are returning the daatframe after changing the timestamp_readable and original_timestamp_readable. Also we 
        are adding a column called time stamp which changes the timestamp_readable to an timestamp.

    """
    licensing_source_df = pd.DataFrame.from_dict(my_data)
    # licensing_source_df['timestamp_readable'] = licensing_source_df['timestamp_readable'].apply(pd.to_datetime)
    # licensing_source_df['original_timestamp_readable'] = licensing_source_df['original_timestamp_readable'].apply(pd.to_datetime)
    
    # timestamp = licensing_source_df.timestamp_readable.map(lambda x: x.replace(tzinfo=timezone.utc).timestamp()) 
    # licensing_source_df.insert (8, "timestamp", timestamp)
    return licensing_source_df



def insert_df_to_db(licensing_source_df):
    """
    

    Parameters
    ----------
    licensing_source_df :  dataframe
        We are passing the complete df to this function to insert the data in the dabase table industry_news_trends .
        The query will make sure not to insert any duplicates. We do this by checking the that title_link does not exist
        if the title link exists it will not be inserted.

    Returns
    -------
    None.


    """
    
    # creating column list for insertion 
    cols = "`,`".join([str(i) for i in licensing_source_df.columns.tolist()])
    # Insert DataFrame records one by one. 
    for i,row in licensing_source_df.iterrows():
        sql = "INSERT INTO `news` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cur.execute(sql, tuple(row)) 
# the connection is not autocommitted by default, so we must commit to save our # changes 
        db.commit()
    # for i in licensing_source_df.index:
    #     title = licensing_source_df.loc[i,'title']
    #     title_link = licensing_source_df.loc[i,'title_link']
    #     author = licensing_source_df.loc[i,'author']
    #     text = licensing_source_df.loc[i,'text']
    #     image = licensing_source_df.loc[i,'image']
    #     service_name = licensing_source_df.loc[i,'service_name']
    #     service_icon= licensing_source_df.loc[i,'service_icon']
    #     approved= licensing_source_df.loc[i,'approved']
    #     # timestamp= float(licensing_source_df.loc[i,'timestamp'])
    #     # timestamp_readable= licensing_source_df.loc[i,'timestamp_readable']
    #     # #timestamp_readable=drum_data_df.to_pydatetime()
    #     # original_timestamp_readable= licensing_source_df.loc[i,'original_timestamp_readable']
    #     # #original_timestamp_readable=original_timestamp_readable.to_pydatetime()
    #     # created_at= licensing_source_df.loc[i,'created_at']
    #     # updated_at= licensing_source_df.loc[i,'updated_at']
    #     # from_slack= licensing_source_df.loc[i,'from_slack']
        
    #     try:
    #         SQL = """INSERT INTO portal_IFDEV01.industry_news_trends (title,title_link,author,text,image,service_name,service_icon,approved, timestamp,timestamp_readable,original_timestamp_readable,created_at,updated_at,from_slack
    #                 )  SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS (
    #         SELECT title_link FROM portal_IFDEV01.industry_news_trends WHERE title_link = %s ) LIMIT 1 """
    #         Vals = (title,title_link,author,text,image,service_name,service_icon,approved, timestamp,timestamp_readable,original_timestamp_readable,created_at,updated_at,from_slack,title_link)
    #         cur.execute(SQL, Vals)
    #         db.commit()
    #     except Exception as e:
    #         print(e)   
    

if __name__ == "__main__":  
    urls = get_urls(soup)
    my_data = scrap_website(urls)
    licensing_source_df = list_to_df(my_data)
    insert_df_to_db(licensing_source_df)
    print('all done')