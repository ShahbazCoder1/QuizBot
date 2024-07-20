import os
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
    
    videos = []
    
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        videos.append([InlineKeyboardButton(f"{video_title}", url=f"{video_url}")])
        
    return videos

# Function to evaluate quiz score and suggest videos if needed
def evaluate_quiz_score(score, topic, api_key):
    if score < 5:
        print(f"Your score is {score}. Here are some recommended videos to improve your knowledge on {topic}:")
        videos = get_youtube_video_recommendation(topic, api_key)
        for title, url in videos:
            print(f"{title}: {url}")
    else:
        print(f"Your score is {score}. Great job!")

# Example usage
if __name__ == "__main__":
    # Example score and topic
    score = 3  # User's quiz score
    topic = "Python Programming"  # Topic of the quiz
    api_key = 'Api_Key'  # Replace with your YouTube Data API key
    
    evaluate_quiz_score(score, topic, api_key)
