import time
import requests
import pandas as pd
import json
import random
import boto3
import os

s3_client = boto3.client('s3')


def get_url(channel_id):
    api_key = os.environ['API_KEY']
    url_base = 'https://youtube.googleapis.com/'
    api_service_name = 'youtube/'
    version = 'v3/'
    params = 'channels?part=statistics&id='+channel_id+'&key='+api_key
    
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


def get_channels_statisticals(df_channels_info):
    date = []
    views = []
    subscribers = []
    video_count = []
    channel_name = []
    

    for i in range(len(df_channels_info)):
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
    

def lambda_handler(event, context):
        bucket_name = os.environ['BUCKET_INPUT']
        filename = os.environ['FILE_CHANNELS']

        obj_file = s3_client.get_object(Bucket = bucket_name, Key = filename)
        df_channels = pd.read_csv(obj_file['Body'])

        results = get_channels_statisticals(df_channels)

        date = pd.to_datetime('today').strftime('%Y%m%d')
        results.to_csv(f'/tmp/youtube_stats_{date}.csv', index = False)

        s3 = boto3.resource('s3')
        s3.Bucket(os.environ['BUCKET_OUTPUT']).upload_file(f'/tmp/youtube_stats_{date}.csv', Key = f'youtube_stats_{date}.csv')
        os.remove(f'/tmp/youtube_stats_{date}.csv')

        return f'/tmp/youtube_stats_{date}.csv ==>> successful export! =)'
