from credentials import YT_API_KEY
from data_channel import CHANNELS_NAME, CHANNELS_ID
import time
from tqdm import tqdm
import requests
import pandas as pd
import json
import random


def get_url(channel_id):
    url_base = 'https://youtube.googleapis.com/'
    api_service_name = 'youtube/'
    version = 'v3/'
    params = 'channels?part=statistics&id='+channel_id+'&key='+YT_API_KEY
    
    return (url_base + api_service_name + version + params)


def get_stats(channel_id):
    url = get_url(channel_id)
    channel_info = (requests.get(url).json())['items'][0]['statistics']

    date = pd.to_datetime('today').strftime('%Y-%m-%d')

    channel_stats = {
    'createdAt': date,
    'totalViews': int(channel_info['viewCount']),
    'subscribers': int(channel_info['subscriberCount']),
    'videoCount': int(channel_info['videoCount'])
    }
    
    return channel_stats


def create_df_with_info_channels():
    dicc = {
        'channelName' : CHANNELS_NAME,
        'channelId' : CHANNELS_ID
    }

    file = pd.DataFrame(dicc)
    file.to_csv('channels_to_analize.csv', index=False)
    
    return (file)


def get_channels_statisticals(df_channels_info):
    date = []
    views = []
    subscribers = []
    video_count = []
    channel_name = []
    

    for i in tqdm(range(len(df_channels_info)), colour = 'green'):
        info = get_stats(df_channels_info['channelId'][i])
        video_count.append(info['videoCount'])
        date.append(info['createdAt'])
        views.append(info['totalViews'])
        subscribers.append(info['subscribers'])
        channel_name.append(df_channels_info['channelName'][i])
        time.sleep(random.choice([1, 2, 3, 4]))


    data = {
        'createdAt': date,
        'ChannelName': channel_name,
        'totalViews': views,
        'subscribers': subscribers,
        'videoCount': video_count
    }

    return (pd.DataFrame(data))
    