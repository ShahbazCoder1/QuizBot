'''
Title: YouTube Video Recommendation
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: This function is used to get YouTube video recommendations based on a given topic.
Code Version: V1.0
Copyright ©: Open-source
'''

from googleapiclient.discovery import build
from telegram import InlineKeyboardButton

# Function to get YouTube video recommendations
def get_youtube_video_recommendation(topic, api_key, max_results=3):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Search for videos related to the topic
    request = youtube.search().list(
        q=topic,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    
    # Use list comprehension for efficiency
    return [
        [InlineKeyboardButton(
            f"▶️ {item['snippet']['title'][:20] + '...' if len(item['snippet']['title']) > 10 else item['snippet']['title']}",
            url=f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        )]
        for item in response['items']
    ]